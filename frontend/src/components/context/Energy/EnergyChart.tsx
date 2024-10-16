import React from 'react';
import {AxisOptions, Chart} from "react-charts";
import Measurement from "../../../interfaces/Measurement.ts";
import getLabeledData from "../../../utils/getLabeledData.ts";
import ResizableBox from "../../ResizeableBox.tsx";

type MyDatum = { time: any, energy: number }
const EnergyChart: React.FC<{
    data: Measurement[],
    average: number
}> = ({data, average}) => {
    const [{activeSeriesIndex, activeDatumIndex}, setState] = React.useState({
        activeSeriesIndex: -1,
        activeDatumIndex: -1,
    });

    const labeledData = React.useMemo(() => getLabeledData(data), [data])
    const averageData = labeledData[0].data.map(datum => ({
        time: datum.time,
        energy: average
    }));

    labeledData.push({label: 'Average', data: averageData})
    const primaryAxis = React.useMemo((): AxisOptions<MyDatum> => (
            {
                getValue: datum => datum.time,
            }),
        [])
    const secondaryAxes = React.useMemo((): AxisOptions<MyDatum>[] =>
        [{
            getValue: datum => datum.energy,
            elementType: "line",
            formatters: {
                scale: value => {
                    if (value)
                        return Number(value).toFixed(6)
                }
            }
        }], [])
    return (
        <ResizableBox>
            <Chart options={{
                interactionMode: 'primary',
                data: labeledData,
                primaryAxis,
                secondaryAxes,
                getDatumStyle: (datum, status) =>
                    (activeDatumIndex === datum.index &&
                    activeSeriesIndex === datum.seriesIndex
                        ? {
                            opacity: 1,
                            circle: {
                                r: 5,
                            },
                            rectangle: {
                                stroke: "black",
                                strokeWidth: 3,
                            },
                        }
                        : activeDatumIndex === datum.index
                            ? {
                                opacity: 1,
                                circle: {
                                    r: 3,
                                },
                                rectangle: {
                                    stroke: "black",
                                    strokeWidth: 1,
                                },
                            }
                            : datum.seriesIndex === activeSeriesIndex
                                ? {
                                    circle: {
                                        r: 3,
                                    },
                                    rectangle: {
                                        stroke: "black",
                                        strokeWidth: 1,
                                    },
                                }
                                : status === "groupFocused"
                                    ? {
                                        circle: {
                                            r: 2,
                                        },
                                        rectangle: {
                                            stroke: "black",
                                            strokeWidth: 0,
                                        },
                                    }
                                    : {
                                        circle: {
                                            r: 2,
                                        },
                                        rectangle: {
                                            stroke: "black",
                                            strokeWidth: 0,
                                        },
                                    }) as any,
                getSeriesStyle: (series) => {
                    if (series.label === "Average") {
                        return {
                            color: "#000000",
                            opacity: 0.7,
                            strokeDasharray: "5,5"
                        };
                    }
                    return {
                        color: `url(#${series.index % 4})`,
                        opacity:
                            activeSeriesIndex > -1
                                ? series.index === activeSeriesIndex
                                    ? 1
                                    : 0.3
                                : 1,
                    };
                },
                onFocusDatum: (focused) =>
                    setState({
                        activeSeriesIndex: focused ? focused.seriesIndex : -1,
                        activeDatumIndex: focused ? focused.index : -1,
                    }),
                renderSVG: () => (
                    <defs>
                        <linearGradient id="0" x1="0" x2="0" y1="1" y2="0">
                            <stop offset="0%" stopColor="#17EAD9"/>
                            <stop offset="100%" stopColor="#6078EA"/>
                        </linearGradient>
                        <linearGradient id="1" x1="0" x2="0" y1="1" y2="0">
                            <stop offset="0%" stopColor="#ff8f10"/>
                            <stop offset="100%" stopColor="#ff3434"/>
                        </linearGradient>
                        <linearGradient id="2" x1="0" x2="0" y1="1" y2="0">
                            <stop offset="0%" stopColor="#42E695"/>
                            <stop offset="100%" stopColor="#3BB2B8"/>
                        </linearGradient>
                        <linearGradient id="3" x1="0" x2="0" y1="1" y2="0">
                            <stop offset="0%" stopColor="#ffb302"/>
                            <stop offset="100%" stopColor="#ead700"/>
                        </linearGradient>
                    </defs>
                ),

            }}/>
        </ResizableBox>
    );
};

export default EnergyChart;