(function (exports) {

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
            },
            "done": function() {
                // nothing
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
            if (data && data.length > 0) {
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
            params.done();
        });
    }

    function initialize(tables, imgUrls) {
        var tableCount = Object.keys(tables).length;
        var imgCount = Object.keys(imgUrls).length;
        var dataCount = new Common.CountDownLatch(tableCount + imgCount, function () {
            $("#pleaseWaitDialog").modal("hide");
        });

        function imgDone() {
            dataCount.countDown();
        }

        jQuery("#pleaseWaitDialog").modal();

        var monthFormatter = function (value) {
            return value;
        };

        Common.downloadImage(imgUrls.percent, "percent-plot", imgDone);
        Common.downloadImage(imgUrls.deficit, "deficit-plot", imgDone);
        Common.downloadImage(imgUrls.deficit_pct, "deficit-pct-plot", imgDone);

        createTable(tables["deficit-pct-table-monthly"], "#deficit-pct-table-monthly", {
            columnFormatters: { 'Month': monthFormatter },
            defaultFormatter: d3.format(",.1%"),
            done: imgDone
        });
        createTable(tables["deficit-pct-table-annual"], "#deficit-pct-table-annual", {
            done: imgDone,
            defaultFormatter: d3.format(",.1%"),
            columnFormatters: { 'Scenario': monthFormatter },
        });

        createTable(tables["deficit-stats-monthly-table"], "#deficit-stats-monthly-table", {
            columnFormatters: { 'Month': monthFormatter },
            defaultFormatter: d3.format(".3r"),
            done: imgDone
        });
        createTable(tables["deficit-stats-annual-table"], "#deficit-stats-annual-table", {
            done: imgDone,
            defaultFormatter: d3.format(".3r"),
            columnFormatters: { 'Scenario': monthFormatter },
        });

        createTable(tables["deficit-stats-monthly-pct-table"], "#deficit-stats-monthly-pct-table",{
            columnFormatters: { 'Month': monthFormatter },
            defaultFormatter: d3.format(",.1%"),
            done: imgDone
        });
        createTable(tables["deficit-stats-annual-pct-table"], "#deficit-stats-annual-pct-table", {
            done: imgDone,
            defaultFormatter: d3.format(",.1%"),
            columnFormatters: { 'Scenario': monthFormatter },
        });

        var pctUrl = dataUrls["dynamic-pct-plot"]; 
        Common.mpld3Plot("dynamic-pct-plot", pctUrl);
    }
    exports.initialize = initialize;

})(this.ProjectCompare = {})
