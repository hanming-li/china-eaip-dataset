type Position = [number, number, number?]

interface Point {
  coordinates: Position
  type: 'Point'
}

interface MultiPoint {
  coordinates: Position[]
  type: 'MultiPoint'
}

interface LineString {
  coordinates: Position[]
  type: 'LineString'
}

interface MultiLineString {
  coordinates: Position[][]
  type: 'MultiLineString'
}

interface Polygon {
  coordinates: Position[][]
  type: 'Polygon'
}

interface MultiPolygon {
  coordinates: Position[][][]
  type: 'MultiPolygon'
}

type Geometry = Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon

interface GeometryCollection {
  geometries: Geometry[]
  type: 'GeometryCollection'
}

interface Feature {
  geometry: Geometry | GeometryCollection
  id?: string
  properties: object
  type: 'Feature'
}

interface FeatureCollection {
  type: 'FeatureCollection'
  features: Feature[]
}

interface 机场 extends Feature {
  geometry: Point
  properties: {
    city: string
    name: string
    iata: string
    icao: string
    reference_temperature_in_celcius: number
    magnetic_variation: number
  }
  id: string
}

export type {
  Feature,
  FeatureCollection,
  Geometry,
  GeometryCollection,
  LineString,
  MultiLineString,
  MultiPoint,
  MultiPolygon,
  Point,
  Polygon,
  Position,
  机场,
}
