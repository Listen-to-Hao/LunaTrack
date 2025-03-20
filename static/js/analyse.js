document.addEventListener("DOMContentLoaded", function () {
    function parseData(id) {
        let element = document.getElementById(id);
        if (!element) return null;
        try {
            let data = JSON.parse(element.textContent.trim());
            return (data && Object.keys(data).length) ? data : null;
        } catch (error) {
            console.error(`❌ Error parsing JSON for ${id}:`, error);
            return null;
        }
    }

    const chartConfigs = {
        cycle_analysis: {
            type: "line",
            options: {},
            label: "Cycle Length (days)",
            dataKey: "cycle_lengths",
            borderColor: "#e63946",
        },
        blood_analysis: {
            type: "line",
            options: {
                scales: {
                    y: {
                        min: 1,
                        max: 3,
                        ticks: {
                            stepSize: 1,
                            callback: function (value) {
                                return ["Light", "Medium", "Heavy"][value - 1];
                            }
                        }
                    }
                }
            },
            label: "Blood Flow Intensity",
            dataKey: "blood_values",
            borderColor: "#0077b6",
        },
        symptom_analysis: {
            type: "bar",
            options: {},
            label: "Symptom Frequency",
            dataKey: "symptom_trends",
            backgroundColor: "purple",
        },
        weight_analysis: {
            type: "line",
            options: {},
            label: "Weight (kg)",
            dataKey: "weight_data",
            borderColor: "#2a9d8f",
        },
        mood_analysis: {
            type: "line",
            options: {
                scales: {
                    y: {
                        min: 0,
                        max: 3,
                        ticks: {
                            stepSize: 1,
                            callback: function (value) {
                                return ["Low", "Medium", "High"][value - 1];
                            }
                        }
                    }
                }
            },
            label: "Stress Levels",
            dataKey: "stress_levels",
            borderColor: "#ffb703",
        }
    };

    Object.keys(chartConfigs).forEach(key => {
        let chartData = parseData(`${key}Data`);
        if (chartData && chartData[chartConfigs[key].dataKey]) {
            let ctx = document.getElementById(`${key}Chart`).getContext("2d");

            let labels;
            let data;

            //   `symptom_analysis`
            if (key === "symptom_analysis") {
                labels = Object.keys(chartData[chartConfigs[key].dataKey]); 
                data = Object.values(chartData[chartConfigs[key].dataKey]); 
            }
            // `weight_analysis`  `mood_analysis`
            else if (chartData.dates) {
                labels = chartData.dates;  
                data = chartData[chartConfigs[key].dataKey];  
            }
            // `cycle_analysis`  `blood_analysis`
            else {
                labels = chartData[chartConfigs[key].dataKey].map((_, i) => `Data ${i + 1}`);
                data = chartData[chartConfigs[key].dataKey];
            }

            new Chart(ctx, {
                type: chartConfigs[key].type,
                data: {
                    labels: labels,
                    datasets: [{
                        label: chartConfigs[key].label,
                        data: data,
                        borderColor: chartConfigs[key].borderColor || "blue",
                        backgroundColor: chartConfigs[key].backgroundColor || null,
                        fill: false,
                        tension: key === "mood_analysis" ? 0.4 : 0
                    }]
                },
                options: chartConfigs[key].options
            });
        } else {
            console.warn(`⚠️ No data available for ${key}.`);
        }
        
        if (key === "cycle_analysis" && chartData.next_period_estimate) {
            let cycleCard = document.getElementById(`${key}Chart`).closest(".analysis-card");
            let nextPeriodInfo = document.createElement("p");
            nextPeriodInfo.innerHTML = `<strong>📅 Next Expected Period: ${chartData.next_period_estimate}</strong>`;
            cycleCard.appendChild(nextPeriodInfo);
        }
    });
    
    const symptomRecommendations = document.querySelector(".symptom-recommendations ul");
    if (symptomRecommendations) {
        symptomRecommendations.querySelectorAll("li").forEach(li => {
            li.style.backgroundColor = "#e9f5ff";
            li.style.padding = "10px";
            li.style.borderRadius = "5px";
            li.style.marginBottom = "10px";
        });
    }
});
