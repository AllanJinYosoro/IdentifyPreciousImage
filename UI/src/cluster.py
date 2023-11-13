from clustimage import Clustimage

def cluster_N_unique_image(folder,clustNum = 45):
    # Initialize
    cl = Clustimage(method='pca-hog',
                    embedding='tsne',
                    grayscale=False,
                    dim=(128,128),
                    params_pca={'n_components':0.95})

    # Import data by "path to directory"
    X = cl.import_data(folder)

    # Preprocessing, feature extraction, embedding and cluster evaluation
    results = cl.fit_transform(X,cluster='agglomerative',
                    evaluate='silhouette',
                    metric='euclidean',
                    linkage='ward',
                    cluster_space='high',
                    min_clust = clustNum,
                    max_clust = clustNum,
                    )

    # Get the unique detected images (in dict)
    uniqueImage = cl.results_unique

    # return 'pathnames' from uniqueImage and transform to list
    uniqueImage_path = uniqueImage['pathnames']

    return uniqueImage_path
