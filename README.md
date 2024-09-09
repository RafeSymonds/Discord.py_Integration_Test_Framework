# Discord.py Integration Testing Framework (WIP)

This system is currently a work in progress. Expect more features to come!

## Overview

This framework facilitates easy end-to-end testing of Discord bots by simulating user commands and validating the expected outcomes. Designed with simplicity in mind, the framework offers ease-of-use similar to `pytest`, making it straightforward to create and manage bot tests.

## How to Use

Below is a basic guide on how to set up and run tests using this framework.

### Setup

1. **Create a Test Directory**: Set up a new directory specifically for your integration tests. The framework will scan every file in this directory for tests, so it's best to separate integration tests from unit tests.

2. **Invoke Test Runner**: Create a command that calls `runner.run_integration_tests()`, passing in the necessary information.

That's all it takes to get the basic system running!

### Test Creation

One of the key features of this framework is the ability to have the Discord bot run commands as the user who initiated the test. This is especially useful for testing interactions that require sending direct messages (DMs), as bots cannot send DMs to themselves.

One feature is to check if a message sends correctly. To check a message sends correctly, you will need to

1. Get the last message in the expected channel before you start asserting the message will send which can either be
    * the command that is being tested
    * or just the last message in a channel if the desired channel is in a different than where the command is being run
2. Wait for the message with `wait_for_new_message` 
    * Will throw an error if the message is not received