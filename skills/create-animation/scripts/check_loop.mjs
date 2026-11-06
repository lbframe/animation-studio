#!/usr/bin/env node
/** Sampled continuity diagnostics for a trusted module exporting sample(t).
 * sample must be deterministic and handle unwrapped t < 0 and t > 1.
 * Return stable JSON-like numeric landmarks, not a wrapped angle or render node.
 */
import { stat } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const usage = `Usage: node check_loop.mjs MODULE [--samples N] [--atol N] [--rtol N] [--step N]
MODULE exports sample(t), returning a stable object/array of finite numbers,
booleans, strings and null. Run only modules you trust: importing executes code.
t is normalized, unwrapped time in cycles, including values outside [0, 1].
--samples 128  Phases checked for F(t) = F(t + 1), integer 8..4096.
--atol 0.000001  Absolute tolerance for positions and velocities per cycle.
--rtol 0.00001   Relative tolerance, applied to the larger compared magnitude.
--step 0.0001    One-sided finite-difference step in cycles, 1e-7..0.01.
Exit: 0 passed sampled checks; 1 detected a state/loop defect; 2 input/runtime error.
Use Cartesian landmarks or canonical values when angles differ by full turns.
This does not assess visual quality, rendered pixels, or playback frame rate.`;

class StateError extends Error {}
const args = process.argv.slice(2);
const options = { samples: 128, atol: 1e-6, rtol: 1e-5, step: 1e-4 };
const checks = {};
const failures = [];
let modulePath, sample, baseline, numericFields = 0;
const cache = new Map();
const scope = 'Finite sampled numeric-state periodicity and C1 seam diagnostics; not a proof for all times, a visual review, a raster check, or a frame-rate measurement.';

function emit(ok, extra = {}) {
  console.log(JSON.stringify({ ok, module: modulePath, scope, options,
    sampledStates: cache.size, numericFields, checks, failures, ...extra }, null, 2));
}

function flatten(value, path = '$', result = new Map(), ancestors = new Set()) {
  if (value === null || typeof value === 'boolean' || typeof value === 'string') {
    result.set(path, { type: value === null ? 'null' : typeof value, value });
  } else if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw new StateError(`${path}: non-finite number`);
    result.set(path, { type: 'number', value });
  } else if (typeof value === 'object') {
    if (ancestors.has(value)) throw new StateError(`${path}: cyclic object`);
    ancestors.add(value);
    if (Array.isArray(value)) {
      result.set(path, { type: 'array', value: value.length });
      for (let i = 0; i < value.length; i++) flatten(value[i], `${path}[${i}]`, result, ancestors);
    } else {
      const proto = Object.getPrototypeOf(value);
      if (proto !== Object.prototype && proto !== null) throw new StateError(`${path}: expected a plain object`);
      const keys = Object.keys(value).sort();
      if (Object.getOwnPropertySymbols(value).length) throw new StateError(`${path}: symbol keys are unsupported`);
      result.set(path, { type: 'object', value: JSON.stringify(keys) });
      for (const key of keys) flatten(value[key], `${path}[${JSON.stringify(key)}]`, result, ancestors);
    }
    ancestors.delete(value);
  } else throw new StateError(`${path}: unsupported ${typeof value}`);
  return result;
}

async function state(t) {
  if (cache.has(t)) return cache.get(t);
  let flat;
  try { flat = flatten(await sample(t)); }
  catch (error) {
    if (error instanceof StateError) throw new StateError(`t=${t}: ${error.message}`);
    throw new Error(`sample(${t}) failed: ${error.message}`);
  }
  if (!baseline) {
    baseline = flat;
    numericFields = [...flat.values()].filter(entry => entry.type === 'number').length;
    if (!numericFields) throw new StateError('sample(t) must contain at least one numeric field');
  } else {
    if (flat.size !== baseline.size) throw new StateError(`t=${t}: state structure changed`);
    for (const [path, entry] of baseline) {
      const next = flat.get(path);
      if (!next || next.type !== entry.type ||
          (['array', 'object'].includes(entry.type) && next.value !== entry.value)) {
        throw new StateError(`t=${t}: state structure changed at ${path}`);
      }
    }
  }
  cache.set(t, flat);
  return flat;
}

function compare(check, path, actual, expected, phase) {
  const metric = checks[check] ??= { ok: true, comparisons: 0, failed: 0, maxAbsError: 0, maxToleranceRatio: 0 };
  metric.comparisons++;
  const numeric = typeof actual === 'number' && typeof expected === 'number';
  const error = numeric ? Math.abs(actual - expected) : Number(actual !== expected);
  const tolerance = numeric ? options.atol + options.rtol * Math.max(Math.abs(actual), Math.abs(expected)) : 0;
  if (!Number.isFinite(error) || !Number.isFinite(tolerance)) {
    metric.ok = false;
    metric.failed++;
    throw new StateError(`${check} at ${path}: numerical overflow; rescale the state or adjust tolerances`);
  }
  const ratio = tolerance ? error / tolerance : (error ? null : 0);
  metric.maxAbsError = Math.max(metric.maxAbsError, error);
  if (ratio === null) metric.maxToleranceRatio = null;
  else if (metric.maxToleranceRatio !== null) metric.maxToleranceRatio = Math.max(metric.maxToleranceRatio, ratio);
  if (error > tolerance) {
    metric.ok = false;
    metric.failed++;
    if (failures.length < 12) failures.push({ check, path, phase, actual, expected, error, tolerance });
  }
}

function compareStates(a, b, phase) {
  for (const [path, entry] of a) {
    if (!['array', 'object'].includes(entry.type)) compare('periodicity', path, entry.value, b.get(path).value, phase);
  }
}

// Extrapolate position from four samples off the seam to expose modulo resets.
// Estimate velocity with a fourth-order one-sided stencil including the seam.
// Subtract the center before arithmetic to reduce cancellation from large offsets.
function extrapolate(states, path, center, h, side) {
  const [a, b, c, d] = states.map(item => item.get(path).value - center);
  return { position: center + 4 * a - 6 * b + 4 * c - d,
    velocity: side * (48 * a - 36 * b + 16 * c - 3 * d) / (12 * h) };
}

async function seam(phase) {
  const h = options.step;
  const center = await state(phase);
  const left = await Promise.all([1, 2, 3, 4].map(n => state(phase - n * h)));
  const right = await Promise.all([1, 2, 3, 4].map(n => state(phase + n * h)));
  for (const [path, entry] of center) {
    if (entry.type === 'number') {
      const l = extrapolate(left, path, entry.value, h, -1);
      const r = extrapolate(right, path, entry.value, h, 1);
      compare('seamPosition', path, l.position, r.position, phase);
      compare('seamPosition', path, l.position, entry.value, phase);
      compare('seamPosition', path, r.position, entry.value, phase);
      compare('seamVelocity', path, l.velocity, r.velocity, phase);
    } else if (!['array', 'object'].includes(entry.type)) {
      compare('seamPosition', path, left[0].get(path).value, right[0].get(path).value, phase);
      compare('seamPosition', path, left[0].get(path).value, entry.value, phase);
    }
  }
}

try {
  if (args.includes('--help') || args.includes('-h')) { console.log(usage); process.exit(0); }
  if (!args.length || args[0].startsWith('--')) throw new Error('A module path is required; use --help.');
  modulePath = resolve(args.shift());
  while (args.length) {
    const flag = args.shift();
    const key = flag.slice(2);
    if (!flag.startsWith('--') || !Object.hasOwn(options, key)) throw new Error(`Unknown option: ${flag}`);
    const raw = args.shift();
    if (raw === undefined || raw.trim() === '' || !Number.isFinite(Number(raw))) throw new Error(`${flag} requires a finite number`);
    options[key] = Number(raw);
  }
  if (!Number.isInteger(options.samples) || options.samples < 8 || options.samples > 4096) throw new Error('--samples must be an integer from 8 to 4096');
  if (options.atol < 0 || options.rtol < 0) throw new Error('--atol and --rtol must be nonnegative');
  if (options.step < 1e-7 || options.step > 0.01) throw new Error('--step must be between 1e-7 and 0.01 cycles');
  if (!(await stat(modulePath)).isFile()) throw new Error('The module path must refer to a file');
  ({ sample } = await import(pathToFileURL(modulePath).href));
  if (typeof sample !== 'function') throw new Error('The module must export a function named sample');
  for (let i = 0; i < options.samples; i++) {
    const phase = i / options.samples;
    compareStates(await state(phase), await state(phase + 1), phase);
  }
  await seam(0);
  await seam(1);
  checks.structureAndFinite = { ok: true, sampledStates: cache.size };
  const ok = Object.values(checks).every(check => check.ok);
  emit(ok, { note: 'Seam derivatives are finite-difference estimates in units per cycle. Inspect marginal failures at a second step size. Canonicalize equivalent angles before sampling.' });
  process.exitCode = ok ? 0 : 1;
} catch (error) {
  if (error instanceof StateError) {
    checks.structureAndFinite = { ok: false, sampledStates: cache.size };
    emit(false, { error: error.message, kind: 'state' });
    process.exitCode = 1;
  } else {
    emit(false, { error: error.message, kind: 'input-or-runtime' });
    process.exitCode = 2;
  }
}
