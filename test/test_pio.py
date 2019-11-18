import unittest
import json

from pdal import pio

dummy_pipeline = """{
  "pipeline": [
    {
      "type": "readers.ply",
      "filename": "dummyinput.ply"
    },
    {
      "type": "filters.outlier",
      "method": "statistical",
      "mean_k": 16,
      "multiplier": 1.0
    },
    {
      "type": "filters.range",
      "limits": "Classification![7:7]"
    },
    {
      "type": "filters.normal"
    },
    {
      "type": "writers.ply",
      "storage_mode": "ascii",
      "precision": 4,
      "filename": "dummyoutput.ply",
      "dims": "X,Y,Z,Red,Green,Blue,NormalX,NormalY,NormalZ"
    }
  ]
}"""



class TestPIOBasics(unittest.TestCase):
    def test_pipeline_construction(self):
        pipeline = (pio.readers.ply(filename="dummyinput.ply") +
                    pio.filters.outlier(method="statistical", mean_k=16, multiplier=1.0) +
                    pio.filters.range(limits="Classification![7:7]") +
                    pio.filters.normal() + pio.writers.ply(storage_mode="ascii", precision=4, filename="dummyoutput.ply",
                                                           dims="X,Y,Z,Red,Green,Blue,NormalX,NormalY,NormalZ"))

        self.assertIsInstance(pipeline, pio.PipelineSpec)
        self.assertEqual(len(list(pipeline.stages)), 5)
        self.assertEqual(json.dumps(pipeline.spec, indent=2), dummy_pipeline)

        pipeline = pipeline + pio.readers.auto(filename="anotherdummmyfile.laz")

        self.assertEqual(len(pipeline.readers), 2) # we can have multiple readers

        null_writer = pio.writers.null()
        self.assertIsNot(pipeline.writer, null_writer)
        pipeline = pipeline + null_writer
        self.assertIs(pipeline.writer, null_writer)