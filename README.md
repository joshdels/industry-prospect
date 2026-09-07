# Industry Prospect 

A simple prospect intelligence tool for turning raw prospect information into structured data, outreach questions, and lessons learned.

## What it does

The workflow is simple:

**Paste → Analyze → Store → Outreach → Learn**

### Features

#### 1. Insert

Paste the details of a prospect.

AI extracts and stores the important information:

* Company
* Industry
* Notes
* Status

New prospects are automatically set to `NEW`.

#### 2. Prospect Bank

Store and manage prospects in one place.

The bank allows you to:

* View prospects
* Filter by industry
* Track basic outcomes
* Record lessons learned

#### 3. Outreach

Generate an outreach-ready message based on the **3 big questions**:

1. How are you doing this today?
2. What is difficult about the current process?
3. What happens if the problem is not solved?

#### 4. Simple Dashboard

See a basic summary of the prospect bank:

* Prospects by industry
* Success / failure
* Lessons learned

## UI

The application will have two main pages:

### Insert

Paste prospect information and let AI structure it.

### Dashboard

View and filter the prospect bank and review the lessons learned.

## Tech Stack

* **Django** — Backend and data models
* **PostgreSQL / Neon** — Database
* **MCP** — AI interaction

## Goal

Keep the system simple.

The goal is not to build a full CRM.

The goal is to create a small feedback loop that helps turn prospect conversations into structured information and better outreach.

**Prospect → Conversation → Lesson → Better Prospecting**
