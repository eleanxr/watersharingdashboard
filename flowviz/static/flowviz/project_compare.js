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

    function initializeCedar(dataUrl) {
        // Consider using Cedar or Vega later if this becomes a real thing.
        // For now we're not using this function at all.
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
    }

    function createTable(dataUrl, selector) {
        d3.csv(dataUrl, function (data) {
            if (data.length > 0) {
                // Get the column names
                var columns = Object.keys(data[0])

                var table = d3.select(selector)
                    .append("table")
                    .attr("class", "table table-striped table-condensed");
                var thead = table.append("thead");
                var tbody = table.append("tbody");

                // Create the header.
                thead.append("tr")
                    .selectAll("th")
                    .data(columns)
                    .enter()
                    .append("th")
                    .text(function (col) { return col; });

                // Fill the rows.
                var rows = tbody.selectAll("tr")
                    .data(data)
                    .enter()
                    .append("tr");
                var cells = rows.selectAll("td")
                    .data(function (row) {
                        return columns.map(function (column) {
                            return {column: column, value: row[column]};
                        });
                    })
                    .enter()
                    .append("td")
                    .text(function (d) { return d.value; });
            }
        });
    }

    function initialize(tables) {
        $.map(tables, function (url, tableId) {
            createTable(url, "#" + tableId);
        });
    }

    return {
        initialize: initialize
    }

})(window)
