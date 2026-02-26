from pymilvus import (
    FieldSchema,
    CollectionSchema,
    DataType,
    Function,
    FunctionType,
)

def build_hybrid_schema(dim: int):
    fields = [
        FieldSchema(
            name="id",
            dtype=DataType.VARCHAR,
            is_primary=True,
            auto_id=True,
            max_length=100,
        ),
        FieldSchema(
            name="content",
            dtype=DataType.VARCHAR,
            max_length=65535,
            analyzer_params={"tokenizer": "standard", "filter": ["lowercase"]},
            enable_match=True,
            enable_analyzer=True,
        ),
        FieldSchema(
            name="metadata",
            dtype=DataType.JSON,
        ),
        FieldSchema(
            name="dense_vector",
            dtype=DataType.FLOAT_VECTOR,
            dim=dim,
        ),
        FieldSchema(
            name="sparse_vector",
            dtype=DataType.SPARSE_FLOAT_VECTOR
        ),
    ]

    bm25_function = Function(
        name="bm25",
        function_type=FunctionType.BM25,
        input_field_names=["content"],
        output_field_names="sparse_vector",
    )

    schema = CollectionSchema(
        fields,
        description="Hybrid search collection",
        functions=[bm25_function]
    )

    return schema