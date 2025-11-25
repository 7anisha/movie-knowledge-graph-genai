
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

def parse_json_array(df, col_name):
    """
    Parses a column that contains a JSON string array like:
    '[{"id": 12, "name": "Action"}, ...]'
    """
    schema = ArrayType(
        StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True)
        ])
    )

    return df.withColumn(col_name, from_json(col(col_name).cast("string"), schema))
