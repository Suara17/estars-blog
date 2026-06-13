import type { SiteConfig } from "@/types/config";
import { fontConfig } from "./fontConfig";

const SITE_LANG = "zh_CN";

export const siteConfig: SiteConfig = {
	title: "Estars的收藏夹",
	subtitle: "这条路要走完，才能看到世界的终点，是海纳百川，还是星火燎原。",
	site_url: "https://estars-blog.pages.dev",
	description:
		"Estars的收藏夹，基于 Firefly 与 Astro 搭建的博客。",
	keywords: ["Estars", "收藏夹", "Astro", "Firefly", "Cloudflare Pages"],
	themeColor: {
		hue: 165,
		fixed: false,
		defaultMode: "system",
	},
	pageWidth: 100,
	card: {
		border: true,
		followTheme: false,
	},
	// 全站访问密码（SHA-256 哈希，留空则不限制）
	sitePassword: "",

	favicon: [{ src: "/favicon/favicon.ico" }],
	navbar: {
		logo: {
			type: "image",
			value: "/uploads/avatar/头像图.jpg",
			alt: "Estars的收藏夹",
		},
		title: "Estars的收藏夹",
		widthFull: false,
		menuAlign: "center",
		followTheme: false,
		stickyNavbar: true,
	},
	siteStartDate: "2026-06-10",
	timezone: "Asia/Shanghai",
	rehypeCallouts: {
		theme: "github",
	},
	showLastModified: true,
	outdatedThreshold: 60,
	sharePoster: true,
	generateOgImages: false,
	bangumi: {
		userId: "",
		mode: "dynamic",
		apiUrl: "https://api.bangumi.one",
		subjectBaseUrl: "https://bangumi.one/subject/",
		categoryOrder: ["anime", "book", "music", "game"],
	},
	pages: {
		friends: false,
		sponsor: false,
		guestbook: false,
		bangumi: false,
		gallery: false,
	},
	categoryBar: true,
	postListLayout: {
		defaultMode: "list",
		mobileDefaultMode: "list",
		showTags: true,
		descriptionLines: 2,
		allowSwitch: true,
		grid: {
			masonry: false,
			columnWidth: 320,
		},
	},
	pagination: {
		postsPerPage: 12,
	},
	analytics: {
		googleAnalyticsId: "",
		microsoftClarityId: "",
		umamiAnalytics: {
			websiteId: "",
			scriptUrl: "https://cloud.umami.is/script.js",
			replaysScriptUrl: "https://cloud.umami.is/recorder.js",
			trackOutboundLinks: true,
			collectWebVitals: false,
			replays: {
				enabled: false,
				sampleRate: 0.15,
				maskLevel: "moderate",
				maxDuration: 300000,
				blockSelector: "",
			},
		},
		la51Analytics: {
			Id: "",
			sdkUrl: "",
			ck: "",
		},
	},
	font: fontConfig,
};

export { SITE_LANG };
