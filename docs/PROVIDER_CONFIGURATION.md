# Provider configuration

ResolveAtlas routes every analysis task to one explicitly registered provider.
An unconfigured task fails; it is never sent to a default or backup service.

## Offline provider

`local-evidence` performs no inference and makes no network request. It renders a
deterministic, cited digest for demonstrations and privacy-safe workflow tests.

## Gemini

The `gemini` adapter uses Google's public `generateContent` REST endpoint at the
fixed host `generativelanguage.googleapis.com`. The API key is sent in the
`x-goog-api-key` header, never in the URL. Operators must supply the model name
and key through their runtime secret/configuration system.

## AWS Bedrock

The `bedrock` adapter uses the public Bedrock Runtime `Converse` operation. With
the optional `aws` dependency, `BedrockProvider.from_boto3` uses boto3's normal
credential chain. ResolveAtlas does not add a proxy, custom credential format,
private endpoint, or internal model alias.

## Data boundary

Both cloud adapters receive the rendered instructions, subject identifier,
evidence title/body, source system, source record identifier, and citation ID.
Callers should minimize or redact evidence before constructing the bundle when
their policy requires it. Credentials are not part of the evidence model.
