# GitHub Actions

Limitations of the free version:
- Organization-wide templates and actions are not available for private repos in free version.
- 500 min/month of Actions (triggers for self-hosted runners are free)

## First things first

Created an Organization: [WITH-Test](https://github.com/WITH-Test)

## How do GitHub Actions work?

Create a base public repo, `.github`, for the Organization:
- here we'll have `workflow-templates`, to give easy access and configuration to projects

Everything is handled in separate repositories, that can make use of each other.

