# Supported environments and limitations

ResolveAtlas currently targets CPython 3.11 through 3.13 on general-purpose
operating systems supported by those Python releases. The core and offline demo
use only the Python standard library.

The optional AWS adapter requires boto3 1.x and a Bedrock model supporting the
public Converse operation. The Gemini adapter targets the public v1beta
`generateContent` REST operation. The Jira adapter targets read-only Jira Cloud
REST v3 issue retrieval and enhanced JQL search; Jira Data Center/Server and
write operations are not supported.

There is no browser UI in focused v1. Attachment extraction is limited to
bounded UTF-8 plain text, Markdown, and JSON. Archives, PDF/Office documents,
images, converters, persistent credential storage, external mutations,
telemetry, background jobs, and production deployment templates are not
implemented.
