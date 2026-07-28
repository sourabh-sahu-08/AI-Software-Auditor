const assert = require('assert');
const { multiply } = require('./math');

// Simple test runner mimicking what npm test might do
try {
    assert.strictEqual(multiply(2, 3), 6);
    console.log("1 passed");
} catch (error) {
    console.error("1 failing");
    process.exit(1);
}
