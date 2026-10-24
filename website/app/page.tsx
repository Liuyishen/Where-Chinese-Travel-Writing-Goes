"use client";

import { useEffect, useMemo, useState } from "react";

type RelationState = "visited" | "mentioned" | "imagined_or_compared" | "uncertain";
type Geometry = { type: string; coordinates: unknown };
type FeatureProperty = string | number | boolean | null | undefined;
type MapFeature = { type: "Feature"; geometry: Geometry; properties: Record<string, FeatureProperty> };
type FeatureCollection = { type: "FeatureCollection"; metadata: Record<string, unknown>; features: MapFeature[] };
type FullLayer = "relations" | "entities";

const ERAS = ["All", "1980s", "1990s", "2000s", "2010s", "2020s"] as const;
const STATES: RelationState[] = ["visited", "mentioned", "imagined_or_compared", "uncertain"];
const stateLabel: Record<RelationState, string> = { visited: "抵达／停留／现场观察", mentioned: "仅提及", imagined_or_compared: "想象／比较", uncertain: "待判定" };
const stateShort: Record<RelationState, string> = { visited: "visited", mentioned: "mentioned", imagined_or_compared: "imagined / compared", uncertain: "uncertain" };

function asText(value: unknown): string { return value === null || value === undefined ? "" : String(value); }
function project(position: unknown): [number, number] {
  const [longitude, latitude] = position as [number, number];
  return [((longitude + 180) / 360) * 1000, ((90 - latitude) / 180) * 500];
}
function linePath(coordinates: unknown[]): string { return coordinates.map((position, index) => { const [x, y] = project(position); return `${index === 0 ? "M" : "L"}${x.toFixed(2)} ${y.toFixed(2)}`; }).join(" "); }
function polygonPath(coordinates: unknown[]): string { return coordinates.map((ring) => `${linePath(ring as unknown[])} Z`).join(" "); }
function featureDisplayName(feature: MapFeature): string { const p = feature.properties; return asText(p.place_name || p.map_entity_name || p.resolved_name || p.place_name_raw || "未命名地点"); }
function featureKey(feature: MapFeature, index: number): string { const p = feature.properties; return asText(p.canonical_relationship_id || p.metadata_place_id || p.map_entity_id || index); }

export default function Home() {
  const [relations, setRelations] = useState<FeatureCollection | null>(null);
  const [entities, setEntities] = useState<FeatureCollection | null>(null);
  const [signals, setSignals] = useState<FeatureCollection | null>(null);
  const [summary, setSummary] = useState<Record<string, unknown> | null>(null);
  const [fullLayer, setFullLayer] = useState<FullLayer>("relations");
  const [showSignals, setShowSignals] = useState(true);
  const [era, setEra] = useState<(typeof ERAS)[number]>("All");
  const [state, setState] = useState<"All" | RelationState>("All");
  const [entityType, setEntityType] = useState("All");
  const [countryQuery, setCountryQuery] = useState("");
  const [grade, setGrade] = useState("All");
  const [active, setActive] = useState<MapFeature | null>(null);
  const [zh, setZh] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("/data/q1_fulltext_text_place_relations.geojson").then((response) => response.json() as Promise<FeatureCollection>),
      fetch("/data/q1_fulltext_entities.geojson").then((response) => response.json() as Promise<FeatureCollection>),
      fetch("/data/q1_metadata_place_signals.geojson").then((response) => response.json() as Promise<FeatureCollection>),
      fetch("/data/q1_map_release_summary.json").then((response) => response.json() as Promise<Record<string, unknown>>),
    ]).then(([nextRelations, nextEntities, nextSignals, nextSummary]) => {
      setRelations(nextRelations); setEntities(nextEntities); setSignals(nextSignals); setSummary(nextSummary);
    }).catch(() => setRelations({ type: "FeatureCollection", metadata: { error: true }, features: [] }));
  }, []);

  const tx = (en: string, cn: string) => (zh ? cn : en);
  const entityTypes = useMemo(() => {
    const source = fullLayer === "relations" ? relations?.features : entities?.features;
    return ["All", ...new Set((source || []).map((feature) => asText(feature.properties.entity_type)).filter(Boolean))];
  }, [relations, entities, fullLayer]);
  const fullVisible = useMemo(() => {
    const source = fullLayer === "relations" ? relations?.features || [] : entities?.features || [];
    return source.filter((feature) => {
      const p = feature.properties;
      const eraMatches = fullLayer === "entities" || era === "All" || p.era === era;
      const stateMatches = fullLayer === "entities" || state === "All" || p.place_status === state;
      const entityMatches = entityType === "All" || p.entity_type === entityType;
      const countryMatches = !countryQuery || asText(p.country_or_region).includes(countryQuery) || asText(p.map_entity_name).includes(countryQuery);
      return eraMatches && stateMatches && entityMatches && countryMatches;
    });
  }, [relations, entities, fullLayer, era, state, entityType, countryQuery]);
  const signalVisible = useMemo(() => (signals?.features || []).filter((feature) => {
    const p = feature.properties; const year = Number(p.year);
    return (era === "All" || `${Math.floor(year / 10) * 10}s` === era) && (grade === "All" || p.evidence_grade_code === grade) && (!countryQuery || featureDisplayName(feature).includes(countryQuery) || asText(p.place_name_raw).includes(countryQuery));
  }), [signals, era, grade, countryQuery]);
  const mapFeatures = useMemo(() => [...(showSignals ? signalVisible.map((feature) => ({ feature, source: "signal" as const })) : []), ...fullVisible.map((feature) => ({ feature, source: fullLayer }))], [fullVisible, signalVisible, showSignals, fullLayer]);
  const displayedStates = useMemo(() => Object.fromEntries(STATES.map((kind) => [kind, fullVisible.filter((feature) => feature.properties.place_status === kind).length])) as Record<RelationState, number>, [fullVisible]);
  const distinctPlaces = new Set(fullVisible.map((feature) => asText(feature.properties.map_entity_id || feature.properties.place_id))).size;
  const relationCount = Number((summary?.fulltext_relations as Record<string, unknown> | undefined)?.mapped_public_relations || 0);

  function renderFeature(feature: MapFeature, source: string, index: number) {
    const geometry = feature.geometry; const p = feature.properties;
    const className = ["geo-feature", source, asText(p.place_status || "entity")].join(" ");
    const label = `${featureDisplayName(feature)}${p.title ? ` — ${p.title}` : ""}`;
    const common = { className, onClick: () => setActive(feature), role: "button", tabIndex: 0, onKeyDown: (event: React.KeyboardEvent<SVGElement>) => { if (event.key === "Enter") setActive(feature); }, "aria-label": label };
    if (geometry.type === "Point") { const [x, y] = project(geometry.coordinates); return <g key={`${source}-${featureKey(feature, index)}`} {...common}><circle className="hit" cx={x} cy={y} r="10" /><circle className="marker-ring" cx={x} cy={y} r="4.2" /><circle className="marker" cx={x} cy={y} r="2" /><title>{label}</title></g>; }
    if (geometry.type === "LineString") return <path key={`${source}-${featureKey(feature, index)}`} {...common} d={linePath(geometry.coordinates as unknown[])}><title>{label}</title></path>;
    if (geometry.type === "Polygon") return <path key={`${source}-${featureKey(feature, index)}`} {...common} d={polygonPath(geometry.coordinates as unknown[])}><title>{label}</title></path>;
    if (geometry.type === "MultiPolygon") return <path key={`${source}-${featureKey(feature, index)}`} {...common} d={(geometry.coordinates as unknown[]).map((polygon) => polygonPath(polygon as unknown[])).join(" ")}><title>{label}</title></path>;
    return null;
  }

  const activeProperties = active?.properties || {}; const ready = Boolean(relations && entities && signals && summary);
  return <main>
    <nav className="topbar"><a className="mark" href="#top"><span>W</span>CTW</a><div className="navlinks"><a href="#map">{tx("Map", "地图")}</a><a href="#methods">{tx("Methods & limits", "方法与限制")}</a><button onClick={() => setZh(!zh)}>{zh ? "EN" : "中文"}</button></div></nav>
    <section id="top" className="hero"><p className="eyebrow">RESEARCH ARCHIVE · 1980—2025</p><h1>{tx("Where Chinese-Language Travel Writing Goes", "中文旅行写作去往何处")}</h1><p className="hero-sub">{tx("Place, mobility, and cultural imagination", "地点、移动与文化想象")}</p><p className="hero-intro">{tx("A map of place entities, text-place relations, and bibliographic signals — deliberately kept separate so a place mentioned in metadata never becomes an authorial footprint.", "一张将地点实体、文本—地点关系与书目地点信号严格分层的研究地图：书目中被提到的地点，绝不会被画成作者足迹。")}</p><a className="text-link" href="#map">{tx("Explore the map", "进入地图")} <span>↓</span></a></section>
    <section id="map" className="map-section"><header className="section-head"><div><p className="eyebrow">01 / {tx("Map layers", "地图图层")}</p><h2>{tx("Evidence before itinerary.", "先证据，后路线。")}</h2></div><p>{ready ? <><strong>{relationCount}</strong> {tx("mapped full-text relations", "条可发布全文关系")}</> : tx("Loading map data…", "正在加载地图数据…")}</p></header>
      <div className="boundary-banner"><b>{tx("Current view", "当前视图")}</b><span>{fullLayer === "relations" ? tx("Full-text text–place relations. Point / line / area geometry belongs to the named place; no itinerary line is reconstructed.", "全文文本—地点关系。点、线、面均属于被书写的地点实体；不从零散关系重建行程线。") : tx("Canonical entity inventory. It shows publishable entities, not authorial arrival.", "规范地点实体库存。它显示可发布实体，不代表作者到访。")}</span>{showSignals && <span className="signal-boundary">{tx("All publishable bibliographic signals are shown underneath in the lightest related layer; they remain non-footprint evidence.", "所有可发布书目地点信号默认以最浅的 related 图层叠加在底层；它们始终不是足迹证据。")}</span>}</div>
      <div className="map-shell"><aside className="controls"><div className="control-block"><p>{tx("Full-text layer", "全文层")}</p><button className={`filter ${fullLayer === "relations" ? "selected" : ""}`} onClick={() => setFullLayer("relations")}>{tx("Text–place relations", "文本—地点关系")}</button><button className={`filter ${fullLayer === "entities" ? "selected" : ""}`} onClick={() => setFullLayer("entities")}>{tx("Entity inventory", "地点实体库存")}</button></div><div className="control-block"><p>{tx("Decade", "年代")}</p><div className="decades">{ERAS.map((value) => <button className={era === value ? "active" : ""} key={value} onClick={() => setEra(value)}>{value === "All" ? tx("All", "全部") : value.slice(0, 4)}</button>)}</div></div>{fullLayer === "relations" && <div className="control-block"><p>{tx("Relation status", "关系类型")}</p>{(["All", ...STATES] as const).map((value) => <button className={`filter ${state === value ? "selected" : ""}`} key={value} onClick={() => setState(value)}>{value === "All" ? tx("All relations", "全部关系") : (zh ? stateLabel[value] : stateShort[value])}<small>{value === "All" ? fullVisible.length : displayedStates[value]}</small></button>)}</div>}<div className="control-block"><label htmlFor="entity-type">{tx("Place type", "地点类型")}</label><select id="entity-type" value={entityType} onChange={(event) => setEntityType(event.target.value)}>{entityTypes.map((value) => <option key={value} value={value}>{value === "All" ? tx("All place types", "全部类型") : value}</option>)}</select><label htmlFor="country-query">{tx("Country / region", "国家／地区")}</label><input id="country-query" value={countryQuery} onChange={(event) => setCountryQuery(event.target.value)} placeholder={tx("Filter by name", "输入名称筛选")} /></div><div className="control-block"><button className={`related-toggle ${showSignals ? "selected" : ""}`} onClick={() => setShowSignals(!showSignals)} aria-pressed={showSignals}>{tx("Bibliographic signals", "书目地点信号")}<small>{signalVisible.length} / 210</small></button>{showSignals && <><label htmlFor="grade">{tx("Evidence grade", "证据等级")}</label><select id="grade" value={grade} onChange={(event) => setGrade(event.target.value)}><option value="All">{tx("All grades", "全部等级")}</option>{["M2A", "M2B", "M2C", "M2D"].map((value) => <option value={value} key={value}>{value}</option>)}</select></>}</div><div className="legend"><span className="visited">visited</span><span className="mentioned">mentioned</span><span className="imagined_or_compared">imagined / compared</span><span className="signal">metadata signal</span></div></aside>
        <div className="map-canvas"><svg viewBox="0 0 1000 500" role="img" aria-label={tx("Research map of Chinese travel writing places", "中文旅行写作地点研究地图")}><defs><pattern id="grid" width="83.33" height="55.56" patternUnits="userSpaceOnUse"><path d="M 83.33 0 L 0 0 0 55.56" fill="none" stroke="#827b6e" strokeWidth="0.5" opacity="0.28" /></pattern></defs><rect width="1000" height="500" fill="url(#grid)" />{mapFeatures.map(({ feature, source }, index) => renderFeature(feature, source, index))}</svg><p className="map-note">{tx(`${fullVisible.length} full-text relations · ${showSignals ? `${signalVisible.length} related signals · ` : ""}${distinctPlaces} distinct map entities`, `${fullVisible.length} 条全文关系 · ${showSignals ? `${signalVisible.length} 条 related 信号 · ` : ""}${distinctPlaces} 个不同地图实体`)}</p></div>
        <aside className="archive-panel"><p className="eyebrow">{tx("Evidence card", "证据卡片")}</p>{active ? <><h3>{featureDisplayName(active)}</h3><p className="archive-note">{asText(activeProperties.title) ? `${asText(activeProperties.author)}《${asText(activeProperties.title)}》 · ${asText(activeProperties.year)}` : asText(activeProperties.place_name_raw || activeProperties.map_entity_name)}</p><dl className="evidence-list">{activeProperties.place_status && <><dt>{tx("Relation", "关系")}</dt><dd>{zh ? stateLabel[asText(activeProperties.place_status) as RelationState] : stateShort[asText(activeProperties.place_status) as RelationState]}</dd></>}<dt>{tx("Layer", "图层")}</dt><dd>{asText(activeProperties.feature_layer)}</dd>{activeProperties.entity_type && <><dt>{tx("Entity type", "实体类型")}</dt><dd>{asText(activeProperties.entity_type)}</dd></>}{activeProperties.country_or_region && <><dt>{tx("Region", "国家／地区")}</dt><dd>{asText(activeProperties.country_or_region)}</dd></>}{activeProperties.mobility_mode && <><dt>{tx("Mobility", "移动方式")}</dt><dd>{asText(activeProperties.mobility_mode)}</dd></>}{activeProperties.evidence_locator && <><dt>{tx("Evidence locator", "证据位置")}</dt><dd>{asText(activeProperties.evidence_locator)}</dd></>}{activeProperties.evidence_grade_code && <><dt>{tx("Signal grade", "信号等级")}</dt><dd>{asText(activeProperties.evidence_grade_code)}</dd></>}</dl>{activeProperties.source_url && <a className="source-link" href={asText(activeProperties.source_url)} target="_blank" rel="noreferrer">{tx("Open source record", "打开来源记录")} ↗</a>}<p className="card-boundary">{asText(activeProperties.map_note || activeProperties.publication_note || "")}</p></> : <p className="archive-note">{tx("Select a point, line, or area to inspect its evidence and layer boundary.", "选择一个点、线或面，查看其证据与图层边界。")}</p>}</aside></div>
    </section>
    <section id="methods" className="methods"><p className="eyebrow">02 / {tx("Methods & limits", "方法与限制")}</p><h2>{tx("Three map layers, three different claims.", "三个地图图层，三种不同主张。")}</h2><div className="method-grid"><article><b>{tx("Full-text relation layer", "全文关系层")}</b><p>{tx("A relation is shown only where an analysis-permitted full text, semantic screening, and a publishable place geometry meet. It still keeps its relation category and manual-signoff state.", "仅当合规全文、关系语义筛查与可发布地点几何同时成立时，文本—地点关系才进入地图；它仍保留关系类别与人工签署状态。")}</p></article><article><b>{tx("Entity inventory", "实体库存层")}</b><p>{tx("The canonical entity map contains 125 publishable geographic entities. It is a spatial reference layer, not a travel or route layer.", "规范实体层含 125 个可发布地理实体；它是空间参照层，而非旅行或路线层。")}</p></article><article><b>{tx("Bibliographic signal layer", "书目信号层")}</b><p>{tx("The 210 signals are retrieval and visibility evidence from bibliographic metadata. They never demonstrate that an author arrived at the named place.", "210 条信号来自书目元数据，用于追索与可见性研究；它们绝不证明作者抵达过该地。")}</p></article></div><p className="methods-footnote">{tx("Absence from the map means only that the current release lacks a publishable geometry or evidence state; it does not mean that a place was absent from travel writing.", "未出现在地图上只表示当前版本缺少可发布几何或足够的证据状态；不表示该地从未进入旅行写作。")}</p></section><footer><span>WHERE CHINESE-LANGUAGE TRAVEL WRITING GOES</span><span>RESEARCH MAP RELEASE · 2026-10-06</span></footer>
  </main>;
}
