from dataclasses import dataclass


@dataclass
class GTEConfig:
    base_model = "thenlper/gte-base"
    cache_folder = "/tmp/gte/model"
