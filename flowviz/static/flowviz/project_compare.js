var ProjectCompare = (function (window, undefined) {

    function pandasIndexToCedar(dataset) {
        var features = []
        for (var indexValue in dataset) {
            if (dataset.hasOwnProperty(indexValue)) {
                var record = dataset[indexValue];
                record['index'] = indexValue;
                features.push({
                    "attributes": record
                });
            }
        }
        return features;
    }

    function initialize(dataUrl) {

        /* Consider using Cedar or Vega later if this becomes a real thing.
        var chart = new Cedar({"type": "bar"});
        var data = Cedar.getJson(dataUrl, function (err, data) {
            if (!err) {
                var cedarData = pandasIndexToCedar(data);

                console.log(cedarData);

                var dataset = {
                    "data": cedarData,
                    "mappings": {
                        "x": {"field": "index", "label": "Date"},
                        "y": {"field": "Mill Creek - Baseline", "label": "% of days in deficit"}
                    }
                };
                chart.dataset = dataset
                chart.show({
                    elementId: "#pct-plot"
                });
            } else {
                console.error("Error loading data");
            }
        });

        vg.parse.spec("/static/flowviz/pct_deficit.vega.json", function (chart) {
            chart({el: "#vega-plot"}).update();
        })
        */

    }

    return {
        initialize: initialize
    }

})(window)
