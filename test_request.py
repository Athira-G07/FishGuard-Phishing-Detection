from utils.feature_extractor import extract_url_features

url = "https://www.google.com"

features = extract_url_features(url)

print("URL features extracted successfully!")
print("\nExtracted features:")
print(features)

print("\nNumber of features:", len(features))