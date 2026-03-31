import time
import os
from flask import Flask, jsonify, request
from src.icp_query import ICP

app = Flask(__name__)

# Ensure log directory exists
os.makedirs('assets', exist_ok=True)

def writelog(domain, result):
    the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_path = os.path.join('assets', 'log.txt')
    with open(log_path, 'a') as f:
        f.write(f'{the_time}  {domain}  {result.get("code", "unknown")}\n')

@app.route('/geticp', methods=['GET'])
def get_icp():
    domain = request.args.get('domain', 'qq.com')
    start_time = time.time()
    
    icp_handler = ICP()
    try:
        result = icp_handler.main(domain)
        writelog(domain, result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        icp_handler.close_session()
        print(f"Query for {domain} took: {time.time() - start_time:.2f}s")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8011))
    app.run(debug=False, host='0.0.0.0', port=port)
