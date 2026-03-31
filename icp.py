import argparse
import sys
import os
import json

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.icp_query import ICP

def query(domain: str, output_json: bool = True):
    """
    Core query function for both CLI and Skill integration.
    """
    icp_handler = ICP()
    try:
        result = icp_handler.main(domain)
        if output_json:
            return json.dumps(result, ensure_ascii=False)
        return result
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)}, ensure_ascii=False)
    finally:
        icp_handler.close_session()

def main():
    parser = argparse.ArgumentParser(description="ICP Query Skill for AI Agents.")
    parser.add_argument("domain", help="The domain name to query (e.g., baidu.com)")
    parser.add_argument("--json", action="store_true", default=True, help="Output JSON result")
    
    args = parser.parse_args()
    print(query(args.domain, args.json))

if __name__ == "__main__":
    main()
