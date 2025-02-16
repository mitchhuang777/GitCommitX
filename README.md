# GitCommitX

## Professional Git Commit Message Generator
GitCommitX is a CLI tool that simplifies commit message writing using **GPT-4o-mini**. It automatically generates meaningful and structured commit message, help developers maintain a clean and consistent commit history.

## How it works
1. Install the required packages `pip install -r requirements.txt`
2. Generate an OpenAI API key [here](https://platform.openai.com/api-keys)
3. Add the OpenAI API key into the `.env.dev` file
4. Stage your changes using `git add <file>` or `git add .` or a GUI tool
5. Run the command to auto generate commit message `python -m gitcommitx.cli commit`
6. Choose between **auto-generating** the commit message or **manually** assigning a type
7. Review and approve the commit message before finalizing the commit

## Commit Message Type Rules

`feat`: Use feat when adding a new feature.

`fix`: Use fix when fixing a bug.

`refactor`: Use refactor when restructuring the code without adding new features.

`docs`: Use docs when modifying documentation files (.md) or comments only.

`style`: Use style when making formatting adjustments (e.g., PEP8 fixes, spacing, line breaks).

`test`: Use test when modifying test files.

`chore`: Use chore for build tools, Git hooks, scripts, or configuration files.

`build`: Use build for changes affecting environment setup, Docker, package managers (e.g., npm, pip).

`ci`: Use ci for modifications related to CI/CD configurations.

`perf`: Use perf when optimizing performance.

`revert`: Use revert when reverting a previous commit.

## Scope Rules

Scope should be based on the filename, not the folder structure.

Example:

`gitcommitx/hooks.py → type(hooks): <description>`

`gitcommitx/config.js → type(config): <description>`

`database/models.ts → type(models): <description>`

`router/user.go → type(user): <description>`

## License
Permission is hereby granted, free of charge, to any individual obtaining a copy
of this software and associated documentation files (the "Software"), to use the
Software solely for personal, non-commercial purposes.

More License details can check [here](https://github.com/mitchhuang777/GitCommitX?tab=License-1-ov-file)
