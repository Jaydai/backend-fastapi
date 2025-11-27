"""
Setup script for creating OpenAI Assistants for enrichment services

This script helps you create or update the OpenAI Assistants used for:
- Message risk assessment (MESSAGE_ENRICHMENT_ASSISTANT_ID)
- Chat classification and quality evaluation (CHAT_CLASSIFICATION_ASSISTANT_ID)

Usage:
    python scripts/setup_assistants.py --create-all
    python scripts/setup_assistants.py --create-risk
    python scripts/setup_assistants.py --create-classification
    python scripts/setup_assistants.py --update-risk <assistant_id>
    python scripts/setup_assistants.py --update-classification <assistant_id>
"""

import argparse

from openai import OpenAI

# Model to use for assistants
DEFAULT_MODEL = "gpt-4.1-nano"


def load_instructions(file_path: str) -> str:
    """Load instructions from a file"""
    with open(file_path) as f:
        return f.read()


def create_risk_assessment_assistant(client: OpenAI, model: str = DEFAULT_MODEL) -> str:
    """Create risk assessment assistant"""
    instructions = load_instructions("prompts/assistants/risk_assessment_instructions.txt")

    assistant = client.beta.assistants.create(
        name="Message Risk Assessment", instructions=instructions, model=model, response_format={"type": "json_object"}
    )

    print(f"✅ Created risk assessment assistant: {assistant.id}")
    print(f"   Add to .env: MESSAGE_ENRICHMENT_ASSISTANT_ID={assistant.id}")
    return assistant.id


def create_classification_assistant(client: OpenAI, model: str = DEFAULT_MODEL) -> str:
    """Create classification assistant"""
    instructions = load_instructions("prompts/assistants/classification_instructions.txt")

    assistant = client.beta.assistants.create(
        name="Chat Classification & Quality",
        instructions=instructions,
        model=model,
        response_format={"type": "json_object"},
    )

    print(f"✅ Created classification assistant: {assistant.id}")
    print(f"   Add to .env: CHAT_CLASSIFICATION_ASSISTANT_ID={assistant.id}")
    return assistant.id


def update_risk_assessment_assistant(client: OpenAI, assistant_id: str, model: str = DEFAULT_MODEL) -> None:
    """Update existing risk assessment assistant"""
    instructions = load_instructions("prompts/assistants/risk_assessment_instructions.txt")

    client.beta.assistants.update(
        assistant_id=assistant_id, instructions=instructions, model=model, response_format={"type": "json_object"}
    )

    print(f"✅ Updated risk assessment assistant: {assistant_id}")


def update_classification_assistant(client: OpenAI, assistant_id: str, model: str = DEFAULT_MODEL) -> None:
    """Update existing classification assistant"""
    instructions = load_instructions("prompts/assistants/classification_instructions.txt")

    client.beta.assistants.update(
        assistant_id=assistant_id, instructions=instructions, model=model, response_format={"type": "json_object"}
    )

    print(f"✅ Updated classification assistant: {assistant_id}")


def main():
    parser = argparse.ArgumentParser(description="Setup OpenAI Assistants for enrichment")
    parser.add_argument("--create-all", action="store_true", help="Create both assistants")
    parser.add_argument("--create-risk", action="store_true", help="Create risk assessment assistant")
    parser.add_argument("--create-classification", action="store_true", help="Create classification assistant")
    parser.add_argument("--update-risk", type=str, help="Update risk assessment assistant (provide assistant ID)")
    parser.add_argument(
        "--update-classification", type=str, help="Update classification assistant (provide assistant ID)"
    )
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")

    args = parser.parse_args()

    # Initialize OpenAI client
    client = OpenAI()

    if args.create_all:
        print("Creating both assistants...")
        create_risk_assessment_assistant(client, args.model)
        create_classification_assistant(client, args.model)
        print("\n✨ Done! Add the assistant IDs to your .env file")

    elif args.create_risk:
        create_risk_assessment_assistant(client, args.model)

    elif args.create_classification:
        create_classification_assistant(client, args.model)

    elif args.update_risk:
        update_risk_assessment_assistant(client, args.update_risk, args.model)

    elif args.update_classification:
        update_classification_assistant(client, args.update_classification, args.model)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
