import json
from chalice import Chalice, CORSConfig
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


app = Chalice(app_name='science')

app.debug = True

# Reuse the Mongo client across Lambda calls.
# TODO: Make DB connection info dependent on environment.
client = MongoClient()
db = client['personal-science']

cors_config = CORSConfig(
    # TODO: Make this environment-dependent.
    allow_origin='http://localhost:3000',
    allow_credentials=True
)

# TODO: Use a more specific CORS definition.
@app.route('/', cors=cors_config)
def index():
    user_id = app.current_request.query_params['userId']
    comparison_tag = app.current_request.query_params['comparisonTag']

    SITE = 'gut'
    TAXON_RANK = 'family'

    # The common JOIN operator.
    lookup = {
            '$lookup': {
                'from': 'microbiomesampledata',
                'let': { 'id': '$_id' },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    { '$eq': ['$$id', '$sampleId'] },
                                    { '$eq': ['$taxonRank', TAXON_RANK] }
                                    ]
                                }
                            }
                        }
                    # TODO: Project.
                    ],
                'as': 'sampleData'
                }
            }

    user_samples = list(db.microbiomesamples.aggregate([
        {
            '$match': {
                'userId': ObjectId(user_id),
                'site': SITE
                }
            },
        lookup

        # TODO: Project.
        ]))

    comparison_samples = list(db.microbiomesamples.aggregate([
        {
            '$match': {
                # Don't match the user's samples a second time.
                'userId': { '$ne': ObjectId(user_id) },
                'tags': {
                    '$elemMatch': { '$eq': comparison_tag }
                    },
                'site': SITE
                }
            },
        lookup

        # TODO: Project.
        ]))

    samples = user_samples + comparison_samples

    count_norms_by_sample = {}

    # Get union of microbe names in matching samples.
    microbe_names = set()
    for sample in samples:
        count_norms_by_sample[sample['_id']] = {}

        for datum in sample['sampleData']:
            # Record the `countNorm` value for quick access later on.
            count_norms_by_sample[sample['_id']][datum['taxonName']] = datum['countNorm']

            # Include the microbe name in our union set.
            microbe_names.add(datum['taxonName'])

    # `data` is a dict whose keys are microbe names and whose values are arrays of microbe
    # `countNorm`s. This can be visualized as a matrix whose rows aer microbe countNorm values and
    # whose columns are samples.
    data = {}
    
    # Generate vectors.
    for microbe_name in microbe_names:
        data[microbe_name] = []

        for sample in samples:
            try:
                count_norm = count_norms_by_sample[sample['_id']][microbe_name]
            except KeyError:
                count_norm = 0

            data[microbe_name].append(count_norm)

    # Create data frame.
    df = pd.DataFrame(data=data)

    # Run ops on data frame to get PCA data.
    x = df.loc[:, microbe_names].values
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components = 2)
    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data = principal_components, columns = ['PC1', 'PC2'])

    # Form data frame for sample groups and titles.
    labels_df_data = {'group': [], 'title': []}
    for sample in samples:
        if str(sample['userId']) == user_id:
            labels_df_data['group'].append('You')
        else:
            labels_df_data['group'].append(comparison_tag)

        labels_df_data['title'].append(sample['title'])

    labels_df = pd.DataFrame(data = labels_df_data)

    # Combine the PCA data with the labels.
    pc_with_labels = pd.concat([principal_df, labels_df], axis=1)

    # Convert to list where each element is a list of the format:
    #   [ <PC1 val>, <PC2 val>, <sample group>, <sample title> ]
    res_data = pc_with_labels.get_values().tolist()

    return res_data
