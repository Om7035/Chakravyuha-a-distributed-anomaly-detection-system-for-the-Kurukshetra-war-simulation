from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float32, Int64

# Define an entity for the soldier
soldier = Entity(name="soldier_id", value_type=ValueType.STRING, description="The ID of the soldier")

# Define the source of the data (Parquet file for offline training)
soldier_stats_source = FileSource(
    path="f:/chakravyu/data/historical.parquet",
    timestamp_field="timestamp",
    created_timestamp_column="created_timestamp",
)

# Define the Feature View
soldier_stats_fv = FeatureView(
    name="soldier_stats",
    entities=[soldier],
    ttl=timedelta(minutes=10),
    schema=[
        Field(name="heart_rate", dtype=Float32),
        Field(name="stamina", dtype=Float32),
    ],
    online=True,
    source=soldier_stats_source,
    tags={"team": "chakravyuha"},
)
