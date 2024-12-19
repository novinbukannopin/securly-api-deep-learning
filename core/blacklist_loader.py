import json

def load_blocklist_to_redis(redis_client, blocklist_file):
    try:
        with open(blocklist_file, "r") as f:
            blocklist = json.load(f)

        redis_key = "blocklist"
        for domain in blocklist:
            redis_client.sadd(redis_key, domain)

        print(f"Blocklist data loaded into Redis under key '{redis_key}'")
    except Exception as e:
        raise RuntimeError(f"Failed to load blocklist into Redis: {e}")
