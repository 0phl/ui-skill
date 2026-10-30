import smoothuiPkg from "../../../packages/smoothui/package.json";
import { source } from "./source";

export interface SmoothuiStats {
  componentCount: number;
  version: string;
}

export function getSmoothuiStats(): SmoothuiStats {
  const componentCount = source
    .getPages()
    .filter(
      (page) =>
        page.url.startsWith("/docs/components/") &&
        page.url !== "/docs/components"
    ).length;

  return {
    componentCount,
    version: smoothuiPkg.version,
  };
}
