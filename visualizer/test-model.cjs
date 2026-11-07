#!/usr/bin/env node
'use strict';

// Runs the mathematical model from the actual visualization, without a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, 'coordinate-lift.html'), 'utf8');
const start = '// BEGIN LIFT MODEL';
const end = '// END LIFT MODEL';
assert.equal(html.split(start).length, 2, 'One model start marker');
assert.equal(html.split(end).length, 2, 'One model end marker');
const code = html.split(start)[1].split(end)[0];
const model = vm.runInNewContext(code + '\nmodel;', {}, { timeout: 2000 });
const plain = value => JSON.parse(JSON.stringify(value));
const close = (actual, expected, message) => {
  const tolerance = 1e-10 * Math.max(1, Math.abs(actual), Math.abs(expected));
  assert.ok(Math.abs(actual - expected) <= tolerance,
    `${message}: expected ${expected}, received ${actual}`);
};

// L appends a fresh coordinate and does not mutate or replace old coordinates.
let coordinates = [];
for (let n = 0; n < 40; n++) {
  const old = coordinates;
  const before = plain(old);
  coordinates = model.append(old);
  assert.notStrictEqual(coordinates, old);
  assert.equal(coordinates.length, n + 1);
  assert.deepEqual(plain(old), before);
  old.forEach((coordinate, i) => assert.strictEqual(coordinates[i], coordinate));
  assert.equal(new Set(coordinates.map(item => item.name)).size, n + 1);
  assert.equal(coordinates[n].name, model.name(n));
  assert.deepEqual(plain(coordinates), plain(model.coordinates(n + 1)));
  close(Math.hypot(...coordinates[n].generator), 1, 'Unit-length projection generator');
}
assert.deepEqual(plain(model.coordinates(0)), []);
assert.deepEqual(plain(model.coordinates(3).map(item => item.generator)),
  [[1, 0, 0], [0, 1, 0], [0, 0, 1]]);

// Camera normalization is stable across persistence echoes, and invalid input is safe.
const views = [model.DEFAULT_VIEW, { yaw: -2.4, pitch: -.7, zoom: 2 }, { yaw: 3, pitch: 1.5, zoom: .25 }];
for (const view of views) assert.deepEqual(plain(model.view(model.view(view))), plain(model.view(view)));
assert.deepEqual(plain(model.view({ yaw: NaN, pitch: Infinity, zoom: 'large' })), plain(model.DEFAULT_VIEW));
assert.equal(model.view({ zoom: 999, pitch: 999 }).zoom, model.MAX_ZOOM);
assert.equal(model.view({ zoom: -9, pitch: -999 }).pitch, -model.MAX_PITCH);
assert.equal(model.view({ zoom: -9 }).zoom, model.MIN_ZOOM);
assert.ok(Math.abs(model.view({ yaw: 500 }).yaw) <= Math.PI);
const originalCoordinates = model.coordinates(40), originalSnapshot = plain(originalCoordinates);
for (const view of views) {
  const transformed = model.projectedGenerators(originalCoordinates, view);
  transformed.forEach((g, i) => close(Math.hypot(...g), Math.hypot(...originalCoordinates[i].generator), 'Camera preserves 3D length'));
  for (let i = 1; i < transformed.length; i++) {
    const dot3 = (a, b) => a.reduce((sum, v, j) => sum + v * b[j], 0);
    close(dot3(transformed[i - 1], transformed[i]), dot3(originalCoordinates[i - 1].generator, originalCoordinates[i].generator), 'Camera preserves 3D angles');
  }
}
assert.deepEqual(plain(originalCoordinates), originalSnapshot, 'Camera never edits the mathematical coordinates');
assert.notDeepEqual(plain(model.projectedGenerators(originalCoordinates, views[0])), plain(model.projectedGenerators(originalCoordinates, views[1])));

// Small discrete grids are the full Cartesian products, including the empty tuple.
for (const [n, expected] of [[0, 1], [1, 3], [2, 9], [3, 27], [6, 729]]) {
  const tuples = model.gridTuples(n);
  assert.equal(tuples.length, expected);
  assert.equal(new Set(tuples.map(tuple => tuple.join(','))).size, expected);
  tuples.forEach(tuple => {
    assert.equal(tuple.length, n);
    tuple.forEach(value => assert.ok([-1, 0, 1].includes(value)));
  });
  for (let i = 0; i < n; i++) {
    const counts = [-1, 0, 1].map(value => tuples.filter(tuple => tuple[i] === value).length);
    assert.deepEqual(counts, [expected / 3, expected / 3, expected / 3]);
  }
}
assert.deepEqual(plain(model.gridTuples(0)), [[]]);

// Bounded higher-dimensional rendering samples are unique and every coordinate varies.
for (const n of [7, 8, 20, 64]) {
  const tuples = model.gridTuples(n);
  assert.equal(tuples.length, model.SAMPLE_LIMIT);
  assert.equal(tuples.length, 729);
  assert.ok(tuples.length < 3 ** n);
  assert.equal(new Set(tuples.map(tuple => tuple.join(','))).size, 729);
  tuples.forEach(tuple => {
    assert.equal(tuple.length, n);
    tuple.forEach(value => assert.ok([-1, 0, 1].includes(value)));
  });
  for (let i = 0; i < n; i++) {
    assert.deepEqual([...new Set(tuples.map(tuple => tuple[i]))].sort(), [-1, 0, 1]);
  }
  // Appending a sampled coordinate preserves the preceding sampled coordinates.
  const next = model.gridTuples(n + 1);
  tuples.forEach((tuple, i) => assert.deepEqual(plain(next[i].slice(0, n)), plain(tuple)));
}

// The displayed cube skeleton has exactly n * 2^(n-1) edges and is connected.
for (let n = 0; n <= 6; n++) {
  const cube = model.cube(n);
  assert.equal(cube.vertices.length, 2 ** n);
  assert.equal(cube.edges.length, n === 0 ? 0 : n * 2 ** (n - 1));
  assert.equal(new Set(cube.vertices.map(vertex => vertex.join(','))).size, 2 ** n);
  const neighbors = Array.from({ length: cube.vertices.length }, () => []);
  const uniqueEdges = new Set();
  cube.vertices.forEach(vertex => {
    assert.equal(vertex.length, n);
    vertex.forEach(value => assert.ok(value === -1 || value === 1));
  });
  cube.edges.forEach(([a, b, axis]) => {
    assert.ok(a >= 0 && a < cube.vertices.length && b >= 0 && b < cube.vertices.length);
    assert.ok(axis >= 0 && axis < n);
    const changed = cube.vertices[a].flatMap((value, i) => value === cube.vertices[b][i] ? [] : [i]);
    assert.deepEqual(plain(changed), [axis]);
    uniqueEdges.add(`${Math.min(a, b)}:${Math.max(a, b)}`);
    neighbors[a].push(b); neighbors[b].push(a);
  });
  assert.equal(uniqueEdges.size, cube.edges.length);
  neighbors.forEach(adjacent => assert.equal(adjacent.length, n));
  const visited = new Set([0]);
  const queue = [0];
  for (let i = 0; i < queue.length; i++) for (const next of neighbors[queue[i]]) {
    if (!visited.has(next)) { visited.add(next); queue.push(next); }
  }
  assert.equal(visited.size, cube.vertices.length);
}
assert.deepEqual(plain(model.cube(7)), { vertices: [], edges: [] });

// The fit radius encloses the projection in every camera orientation; it does not
// depend on yaw/pitch or on the newest-coordinate animation fraction.
for (const n of [0, 1, 3, 6, 8, 40]) {
  const items = model.coordinates(n), cube = model.cube(n), radius = model.radius(items, cube.vertices);
  const tuples = cube.vertices.length ? cube.vertices : model.gridTuples(n);
  for (const view of views) for (const fraction of [0, .4, 1]) {
    const generators = model.projectedGenerators(items, view);
    tuples.forEach(tuple => assert.ok(Math.hypot(...model.project(tuple, generators, fraction)) <= radius + 1e-10));
  }
}

// The outline is the exact planar zonotope, not a guessed hull or an exponential sample.
// Its support in a direction d is sum_i |d dot g_i|, including during the extrusion.
const directions = Array.from({ length: 37 }, (_, i) => {
  const angle = 2 * Math.PI * i / 37;
  return [Math.cos(angle), Math.sin(angle)];
});
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const support = (points, direction) => Math.max(...points.map(point => dot(point, direction)));
for (const view of views) for (const n of [0, 1, 3, 8, 40]) {
  const generators = model.projectedGenerators(model.coordinates(n), view);
  for (const fraction of [0, 0.35, 1]) {
    const outline = model.outline(generators, fraction);
    assert.equal(outline.length, n ? 2 * n + 1 : 1);
    outline.forEach(point => point.forEach(value => assert.ok(Number.isFinite(value))));
    close(outline[0][0], outline.at(-1)[0], 'Closed outline x');
    close(outline[0][1], outline.at(-1)[1], 'Closed outline y');
    for (const direction of directions) {
      const expected = generators.reduce((sum, generator, i) =>
        sum + Math.abs(dot(generator, direction)) * (i === n - 1 ? fraction : 1), 0);
      close(support(outline, direction), expected, `Exact support, n=${n}, fraction=${fraction}`);
    }
  }
}

// A new coordinate expands projected support; setting its animation factor to zero
// recovers exactly the previous projection (rather than constraining old coordinates).
for (const n of [0, 1, 3, 8, 39]) {
  const oldGenerators = model.projectedGenerators(model.coordinates(n));
  const nextGenerators = model.projectedGenerators(model.coordinates(n + 1));
  const fresh = nextGenerators[n];
  const direction = [fresh[0], fresh[1]];
  const before = support(model.outline(oldGenerators), direction);
  const after = support(model.outline(nextGenerators), direction);
  assert.ok(after > before + 1e-9, `New coordinate contributes to the projection for n=${n}`);
  close(after - before, dot(direction, direction), 'New generator support contribution');
  for (const d of directions) {
    close(support(model.outline(nextGenerators, 0), d),
      support(model.outline(oldGenerators), d), 'Zero-factor extrusion preserves old projection');
  }
  const tuple = Array.from({ length: n }, (_, i) => i % 3 - 1);
  const p = model.project(tuple, oldGenerators);
  const q = model.project([...tuple, 1], nextGenerators, 0);
  p.forEach((value, i) => close(q[i], value, 'Old point retained at extrusion start'));
}

console.log('PASS: coordinate generation; exact and sampled grids; cube topology; camera rotations, bounds and stable fit; exact rotated convex support; extrusion invariants.');
