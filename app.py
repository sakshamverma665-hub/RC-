from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ADMIN_USERNAME = "@Saksham24_11"
BASE_API = "https://rc-info-ng.vercel.app/?rc="

@app.route("/vehicle", methods=["GET"])
def vehicle_info():
    rc_number = request.args.get("rc")
    if not rc_number:
        return jsonify({"error": "RC number is required ?rc=MH01AB1234"}), 400

    try:
        # Call original API
        response = requests.get(f"{BASE_API}{rc_number}")
        data = response.json()
    except Exception as e:
        return jsonify({"error": "Failed to fetch vehicle data", "details": str(e)}), 500

    # ✅ Clean unwanted owner username & add our owner
    def clean_data(obj):
        if isinstance(obj, dict):
            cleaned = {}
            for k, v in obj.items():
                # skip unwanted usernames like "owner : @ngyt7777GG"
                if "owner" in k.lower() and isinstance(v, str) and "@" in v:
                    continue
                cleaned[k] = clean_data(v)
            return cleaned
        elif isinstance(obj, list):
            return [clean_data(i) for i in obj]
        else:
            return obj

    cleaned_data = clean_data(data)
    cleaned_data["owner"] = ADMIN_USERNAME  # Always add our owner at the end

    return jsonify(cleaned_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)