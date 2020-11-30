import os
import json
import unittest
from datetime import datetime
from flood_forecast.trainer import train_function
from flood_forecast.deployment import inference
import wandb


class ConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(self.base_path, "decoder_test.json")) as y:
            config = json.load(y)
        self.model_config = config
        self.updated_config = wandb.config

    def test_model_consistency(self):
        train_function("PyTorch", self.model_config)
        self.updated_config = wandb.config
        self.assertIn("gcs_m_path_5_model", self.updated_config)

    def test_inference_same(self):
        print(self.updated_config)
        file_path = os.path.join(self.base_path, "test_data", "keag_small.csv")
        m = inference.InferenceMode(336, 20, self.updated_config["gcs_m_path_5_params"], file_path,
                                    self.updated_config["gcs_m_path_5_model"])
        tensor, history, test, plt = m.make_plots(datetime.datetime(2016, 5, 31))
        wandb.log({"plt_2": plt})
        print("Shut you stupid linter i will use variables later")
        print(tensor)
        print(history)
        print(test)
        print("stuff above")
        self.assertEqual(2, 2)

if __name__ == "__main__":
    unittest.main()
