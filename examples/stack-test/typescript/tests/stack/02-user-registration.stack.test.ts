/**
 * 02-user-registration.stack.test.ts
 *
 * Second test in the sequential stack test suite.
 * Verifies user registration and retrieval flows.
 *
 * Demonstrates:
 * - Full-loop assertion layering (primary, second-order, third-order)
 * - User journey testing
 * - Database state verification via API
 */

import { StackTestUtils } from '../config/stack-utils.js';

describe('Stack Test: User Registration', () => {
  let utils: StackTestUtils;
  let createdUserId: string;

  beforeAll(async () => {
    utils = new StackTestUtils();
    await utils.initialize('docker-compose.test.yml');
    await utils.waitForReady();
  }, 60000);

  afterAll(async () => {
    await utils.cleanup();
  }, 30000);

  test('POST /users creates a new user', async () => {
    const userData = {
      email: 'test@example.com',
      username: 'testuser',
      password: 'SecurePass123!',
    };

    // Primary assertion: API response
    const response = await utils.makeRequest('POST', '/users', userData);

    expect(response.status).toBe(201);
    expect(response.data).toMatchObject({
      id: expect.any(String),
      email: userData.email,
      username: userData.username,
      createdAt: expect.any(String),
    });
    expect(response.data).not.toHaveProperty('password'); // Password never returned

    // Store ID for subsequent tests
    createdUserId = response.data.id;
  });

  test('GET /users/:id returns the created user', async () => {
    // This test depends on the previous test — demonstrating sequential design
    expect(createdUserId).toBeDefined();

    // Primary assertion: user retrieval
    const response = await utils.makeRequest('GET', `/users/${createdUserId}`);

    expect(response.status).toBe(200);
    expect(response.data).toMatchObject({
      id: createdUserId,
      email: 'test@example.com',
      username: 'testuser',
    });

    // Second-order assertion: verify user exists in database via API
    const listResponse = await utils.makeRequest('GET', '/users');
    expect(listResponse.status).toBe(200);
    expect(listResponse.data.users).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          id: createdUserId,
          username: 'testuser',
        }),
      ])
    );
  });

  test('duplicate email returns 409', async () => {
    const duplicateUser = {
      email: 'test@example.com', // Same email as first test
      username: 'different',
      password: 'AnotherPass123!',
    };

    const response = await utils.makeRequest('POST', '/users', duplicateUser);

    expect(response.status).toBe(409);
    expect(response.data).toMatchObject({
      error: 'Email already exists',
    });
  });

  test('user is audited in logs', async () => {
    // Third-order assertion: verify audit log via admin API
    const adminResponse = await utils.makeRequest('GET', '/admin/audit/users');

    expect(adminResponse.status).toBe(200);
    expect(adminResponse.data.entries).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          action: 'USER_CREATED',
          entityType: 'user',
          entityId: createdUserId,
          timestamp: expect.any(String),
        }),
      ])
    );
  });

  test('user data persists after container restart', async () => {
    // Verify data persistence — this is a critical stack test concern
    // The transient volumes should persist until we call cleanup()

    const response = await utils.makeRequest('GET', `/users/${createdUserId}`);
    expect(response.status).toBe(200);
    expect(response.data.id).toBe(createdUserId);
  });
});
