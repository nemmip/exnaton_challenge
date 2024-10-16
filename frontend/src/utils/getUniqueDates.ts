import Measurement from "../interfaces/Measurement.ts";

export default function getUniqueDates(data: Measurement[]) {
    const uniqueDates = new Set(data.map(el => (new Date(el.timestamp)).toLocaleDateString()))
    return [...uniqueDates]
}