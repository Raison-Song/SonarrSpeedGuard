import json
import portalocker
import os
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class Config:
    apikey: str
    host: str
    port: int
    ssl: bool
    refresh_interval: int
    rules: Optional[List[Tuple[bool,Dict]]]

    @classmethod
    def default(cls):
        return cls("", "loaclhost", 8989, False, 5, [
            (
                True,
                {
                    "C1": 5,
                    "C3": 50
                }
            )
        ])


config: Config = Config.default()

config_file_path = 'config/config.json'


def load_config():
    global config
    try:
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Configuration file '{config_file_path}' not found.")

        with open(config_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 检查是否所有必需的字段都存在
        config = Config(**data)

    except FileNotFoundError as e:
        print(e)
        config = Config.default()

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        config = Config.default()

    except TypeError as e:
        print(f"Error loading configuration: {e}")
        config = Config.default()


def update_config(new_config):
    try:
        #  检查文件夹是否存在，如果不存在则创建
        config_dir = os.path.dirname(config_file_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        # 检查配置文件是否存在，如果不存在则创建
        if not os.path.exists(config_file_path):
            try:
                with open(config_file_path, 'w') as f:
                    json.dump({}, f)
            except IOError as e:
                print(f"Error creating config file: {e}")

        with open(config_file_path, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)  # 加锁

            # 重置文件指针并写入新的配置
            f.seek(0)
            json.dump(new_config, f, indent=4)
            f.truncate()  # 清除多余的内容
            portalocker.unlock(f)  # 解锁

    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

    load_config()
