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

    /**
     * Create a table from a url providing a CSV document and a selector
     * for an element in which to place the table.
     * The params object is optional and can contain the following parameters:
     * columnFormatters - An object mapping column names to functions for formatting fields
     * defaultFormatter - A function to use by default for formatting fields.
     */
    function createTable(dataUrl, selector, params) {
        var defaultParams = {
            "columnFormatters": {},
            "defaultFormatter": function (value) {
                return value;
            }
        };

        if (arguments.length === 2) {
            params = defaultParams
        } else {
            params = $.extend(defaultParams, params);
        }

        if (params.hasOwnProperty("columnFormatters")) {
            columnFormatters = params.columnFormatters;
        } else {
            columnFormatters = {};
        }

        d3.csv(dataUrl, function (data) {
            if (data.length > 0) {
                // Get the column names
                var columns = Object.keys(data[0])

                var table = d3.select(selector)
                    .append("table")
                    .attr("class", "table table-striped table-condensed table-hover");
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
                            var value;
                            if (params.columnFormatters.hasOwnProperty(column)) {
                                value = params.columnFormatters[column](row[column]);
                            } else {
                                value = params.defaultFormatter(row[column]);
                            }
                            return {column: column, value: value};
                        });
                    })
                    .enter()
                    .append("td")
                    .text(function (d) { return d.value; });
            }
        });
    }

    function initialize(tables) {
        var monthFormatter = function (value) {
            return value;
        };

        createTable(tables["deficit-pct-table"], "#deficit-pct-table", {
            columnFormatters: { 'month': monthFormatter },
            defaultFormatter: d3.format(",.1%")
        });
        createTable(tables["deficit-stats-table"], "#deficit-stats-table", {
            columnFormatters: { 'month': monthFormatter },
        });
    }

    return {
        initialize: initialize
    }

})(window)