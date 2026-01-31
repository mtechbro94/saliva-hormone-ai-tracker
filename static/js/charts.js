/**
 * Saliva-Based Hormonal Tracking System - Chart.js Charts
 * ========================================================
 * This module handles all Chart.js visualizations:
 * 1. Individual hormone trend charts (Cortisol, Estrogen, Testosterone)
 * 2. Combined comparison chart
 * 
 * Charts update dynamically based on user's hormone records.
 */

// Chart configuration defaults
const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            backgroundColor: 'rgba(30, 41, 59, 0.9)',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 12,
            cornerRadius: 8,
            displayColors: false
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                color: '#64748b',
                font: {
                    size: 11
                }
            }
        },
        y: {
            grid: {
                color: 'rgba(226, 232, 240, 0.5)'
            },
            ticks: {
                color: '#64748b',
                font: {
                    size: 11
                }
            }
        }
    },
    elements: {
        line: {
            tension: 0.4,  // Smooth curves
            borderWidth: 3
        },
        point: {
            radius: 5,
            hoverRadius: 7,
            borderWidth: 2,
            backgroundColor: '#ffffff'
        }
    }
};

// Color schemes for each hormone
const hormoneColors = {
    cortisol: {
        primary: '#f59e0b',     // Amber
        light: 'rgba(245, 158, 11, 0.1)',
        gradient: ['rgba(245, 158, 11, 0.8)', 'rgba(245, 158, 11, 0.1)']
    },
    estrogen: {
        primary: '#8b5cf6',     // Purple
        light: 'rgba(139, 92, 246, 0.1)',
        gradient: ['rgba(139, 92, 246, 0.8)', 'rgba(139, 92, 246, 0.1)']
    },
    testosterone: {
        primary: '#10b981',     // Green
        light: 'rgba(16, 185, 129, 0.1)',
        gradient: ['rgba(16, 185, 129, 0.8)', 'rgba(16, 185, 129, 0.1)']
    }
};

// Normal ranges for reference lines
const normalRanges = {
    cortisol: { min: 3, max: 10 },
    estrogen: { min: 15, max: 350 },
    testosterone: { min: 15, max: 70 }
};

/**
 * Create a gradient for chart fills
 */
function createGradient(ctx, colors) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, colors[0]);
    gradient.addColorStop(1, colors[1]);
    return gradient;
}

/**
 * Create a single hormone chart
 */
function createHormoneChart(canvasId, data, color, label, unit) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');
    const gradient = createGradient(ctx, color.gradient);

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: label,
                data: data.values,
                borderColor: color.primary,
                backgroundColor: gradient,
                fill: true,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: color.primary
            }]
        },
        options: {
            ...chartDefaults,
            plugins: {
                ...chartDefaults.plugins,
                tooltip: {
                    ...chartDefaults.plugins.tooltip,
                    callbacks: {
                        label: function (context) {
                            return `${label}: ${context.parsed.y} ${unit}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create the combined comparison chart
 */
function createCombinedChart(data) {
    const canvas = document.getElementById('combinedChart');
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Cortisol (ng/mL)',
                    data: data.cortisol,
                    borderColor: hormoneColors.cortisol.primary,
                    backgroundColor: 'transparent',
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: hormoneColors.cortisol.primary,
                    yAxisID: 'y'
                },
                {
                    label: 'Estrogen (pg/mL)',
                    data: data.estrogen,
                    borderColor: hormoneColors.estrogen.primary,
                    backgroundColor: 'transparent',
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: hormoneColors.estrogen.primary,
                    yAxisID: 'y1'
                },
                {
                    label: 'Testosterone (ng/dL)',
                    data: data.testosterone,
                    borderColor: hormoneColors.testosterone.primary,
                    backgroundColor: 'transparent',
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: hormoneColors.testosterone.primary,
                    yAxisID: 'y2'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 12,
                    cornerRadius: 8
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#64748b'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Cortisol (ng/mL)',
                        color: hormoneColors.cortisol.primary
                    },
                    ticks: {
                        color: hormoneColors.cortisol.primary
                    },
                    grid: {
                        color: 'rgba(226, 232, 240, 0.3)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Estrogen (pg/mL)',
                        color: hormoneColors.estrogen.primary
                    },
                    ticks: {
                        color: hormoneColors.estrogen.primary
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                y2: {
                    type: 'linear',
                    display: false,  // Hidden to reduce clutter
                    position: 'right'
                }
            },
            elements: {
                line: {
                    tension: 0.4,
                    borderWidth: 2
                },
                point: {
                    radius: 4,
                    hoverRadius: 6,
                    borderWidth: 2,
                    backgroundColor: '#ffffff'
                }
            }
        }
    });
}

/**
 * Fetch hormone data from API and initialize all charts
 */
async function initializeCharts() {
    try {
        // Fetch data from API
        const response = await fetch('/api/hormone_data');
        if (!response.ok) {
            throw new Error('Failed to fetch hormone data');
        }

        const data = await response.json();

        // Check if we have data
        if (!data.labels || data.labels.length === 0) {
            console.log('No hormone data available for charts');
            return;
        }

        // Create individual hormone charts
        createHormoneChart(
            'cortisolChart',
            { labels: data.labels, values: data.cortisol },
            hormoneColors.cortisol,
            'Cortisol',
            'ng/mL'
        );

        createHormoneChart(
            'estrogenChart',
            { labels: data.labels, values: data.estrogen },
            hormoneColors.estrogen,
            'Estrogen',
            'pg/mL'
        );

        createHormoneChart(
            'testosteroneChart',
            { labels: data.labels, values: data.testosterone },
            hormoneColors.testosterone,
            'Testosterone',
            'ng/dL'
        );

        // Create combined chart
        createCombinedChart(data);

        console.log('Charts initialized successfully');

    } catch (error) {
        console.error('Error initializing charts:', error);
    }
}

/**
 * Update charts with new data (can be called after adding new records)
 */
async function refreshCharts() {
    // Destroy existing charts
    Chart.helpers.each(Chart.instances, function (instance) {
        instance.destroy();
    });

    // Reinitialize
    await initializeCharts();
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    // Only initialize if charts exist on the page
    if (document.getElementById('cortisolChart')) {
        initializeCharts();
    }
});
