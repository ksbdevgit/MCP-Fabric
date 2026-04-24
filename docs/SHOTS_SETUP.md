# Few-shot retrieval for `kusto_get_shots`

The `kusto_get_shots` tool retrieves examples ("shots") most semantically
similar to a user prompt, for use as in-context guidance when generating KQL.

It is **not** a static config — it is a retrieval over a Kusto table of
pre-embedded examples. To use it end to end you need:

1. A Kusto table of shots (per-tenant, per-domain, or shared).
2. An Azure OpenAI embedding deployment reachable from the MCP server.
3. The `AZ_OPENAI_EMBEDDING_ENDPOINT` env var set on the App Service.

## 1. Shot table schema

Create a table in any Eventhouse reachable via `KUSTO_KNOWN_SERVICES`:

```kql
.create table fabric_mcp_shots (
    EmbeddingText: string,       // natural-language prompt
    AugmentedText: string,       // the KQL that answers it
    EmbeddingVector: dynamic     // precomputed embedding of EmbeddingText
)
```

Populate it with (prompt, KQL) pairs relevant to this tenant, e.g.:

| EmbeddingText | AugmentedText |
|---|---|
| "listar tablas disponibles en este eventhouse" | `.show external tables` |
| "top 10 clientes por facturación neta 2025" | `external_table('facturacion') \| where year == 2025 \| summarize neto=sum(Neto) by Cliente \| top 10 by neto` |
| "evolución mensual de facturación" | `external_table('facturacion') \| summarize neto=sum(Neto) by bin(FechaFactura, 30d) \| order by FechaFactura asc` |

Each row's `EmbeddingVector` must be the embedding of its `EmbeddingText`
under the same model the MCP server is configured to call.

## 2. Generating the embeddings

The `kusto_get_shots` tool uses the KQL `ai_embeddings()` plugin against
`AZ_OPENAI_EMBEDDING_ENDPOINT`. Fastest way to backfill is a one-time KQL
ingestion script that embeds the prompts inline:

```kql
.set-or-append fabric_mcp_shots <|
    let endpoint = 'https://<your-openai>.openai.azure.com/openai/deployments/<embed-deployment>/embeddings?api-version=2023-05-15';
    datatable (EmbeddingText:string, AugmentedText:string) [
        "listar tablas disponibles", ".show external tables",
        "top clientes por facturación", "external_table('facturacion') | summarize sum(Neto) by Cliente | top 10 by sum_Neto"
    ]
    | extend EmbeddingVector = toscalar(evaluate ai_embeddings(EmbeddingText, endpoint))
```

## 3. Wiring the App Service

In the Portal → App Service `app-FabricMCP-front-prod-001` → Configuration
→ Application settings, add:

| Name | Value |
|---|---|
| `AZ_OPENAI_EMBEDDING_ENDPOINT` | full URL of the Azure OpenAI embedding deployment |

Save and wait for the auto-restart. Callers can then invoke the tool:

```
kusto_get_shots(
    prompt="top 10 clientes por facturación",
    shots_table_name="fabric_mcp_shots",
    cluster_uri="https://trd-nqy8t8x3b6eu50xjbs.z4.kusto.fabric.microsoft.com",
    database="TotalOrders_EventhouseEndpoint"
)
```

## Notes

- The embedding model used to backfill the table **must** match the one the
  server queries at runtime — mismatched vectors return nonsense similarity.
- Managed Identity of the App Service needs `Cognitive Services OpenAI User`
  on the Azure OpenAI resource (or an explicit key, if using key auth).
- Keep the shots table small (tens to low hundreds of rows) — cosine
  similarity is computed over the whole table per call.
