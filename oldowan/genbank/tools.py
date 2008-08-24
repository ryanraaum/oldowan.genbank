def extract_feature_value(entry, feature, value):
    if 'features' in entry:
        for y in entry['features']:
            if y[0] == feature:
                if len(y) > 1:
                    for z in y[1]:
                        if z[0] == value:
                            return z[1]

def make_feature_value_extractor(feature, value):
    return lambda e: extract_feature_value(e, feature, value)
  
