---
title: Adopt the Atlas standard
kind: decision
owner: "{{OWNER}}"
status: published
updated: "{{DATE}}"
audience: [internal]
summary: "Why this repository declares itself against project/1.0."
---

# 1. Adopt the Atlas standard

Date: {{DATE}}

## Status

Accepted.

## Context

A repository accumulates structure by accident unless something states what it
must contain. Every convention that lives only in someone's memory is a
convention that leaves when they do.

## Decision

This repository declares `standard: project/1.0` and is checked against it by
`atlas check` in CI.

## Consequences

The root stays a closed set, ownership resolves to a named principal, and the
manifest classifies the project in terms other repositories share. The cost is a
manifest to keep honest, which is the point.
