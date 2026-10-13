import { defineConfig } from 'vitepress'
// Written by tools/build_plugin.py in davendra/fundadmin-ai from the plugin
// metadata and skill registry. It is the only thing this config knows about
// the plugin, so version, counts and the commands sidebar cannot drift.
import meta from './meta.json'

const site = meta.docs
const categories = meta.categories as { name: string; slug: string; count: number }[]

export default defineConfig({
  title: 'FundAdmin AI Manual',
  description: `User manual for the ${meta.name} plugin: ${meta.skill_count} fund administration skills. Install in Claude Code, ChatGPT desktop, ChatGPT Work or Codex; qualification varies by host.`,
  cleanUrls: true,
  ignoreDeadLinks: false,
  // The published repository is one squashed commit per release, so git dates
  // would all be the release date. The footer carries the version instead.
  lastUpdated: false,
  srcExclude: ['DEPLOY.md', 'README.md'],
  sitemap: { hostname: site },
  head: [
    ['link', { rel: 'icon', href: '/favicon.svg' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'FundAdmin AI Manual' }],
    ['meta', { property: 'og:title', content: 'FundAdmin AI Manual' }],
    ['meta', { property: 'og:description', content: `Install and use the ${meta.name} plugin: ${meta.skill_count} fund administration skills and ${meta.agent_count} LPA-review agents. Claude Code is the primary target; ChatGPT and other hosts remain experimental.` }],
    ['meta', { property: 'og:image', content: `${site}/images/og-social-card.jpg` }],
    ['meta', { property: 'og:url', content: `${site}/` }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:title', content: 'FundAdmin AI Manual' }],
    ['meta', { name: 'twitter:image', content: `${site}/images/og-social-card.jpg` }],
  ],
  themeConfig: {
    logo: { light: '/images/lockup-light.svg', dark: '/images/lockup-dark.svg', alt: 'FundAdmin AI' },
    siteTitle: false,
    search: { provider: 'local' },
    nav: [
      { text: 'Guide', link: '/guide/install' },
      { text: 'Commands', link: '/commands/' },
      { text: 'Agents', link: '/agents' },
      { text: 'Contact', link: 'https://fundadmin.dev/#contact' },
      { text: `v${meta.version}`, link: `${meta.repository}/blob/main/CHANGELOG.md` },
    ],
    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Install', link: '/guide/install' },
            { text: 'Quick start', link: '/guide/quick-start' },
            { text: 'Host checks', link: '/guide/host-checks' },
            { text: 'Output files', link: '/guide/outputs' },
            { text: 'Sample documents', link: '/guide/samples' },
            { text: 'FAQ', link: '/guide/faq' },
            { text: 'Privacy', link: '/guide/privacy' },
          ],
        },
      ],
      '/commands/': [
        {
          text: `All ${meta.skill_count} commands`,
          items: [
            { text: 'Overview', link: '/commands/' },
            ...categories.map((c) => ({ text: `${c.name} · ${c.count}`, link: `/commands/${c.slug}` })),
          ],
        },
      ],
      '/agents': [
        { text: 'Agents', items: [{ text: 'The 5 LPA-review agents', link: '/agents' }] },
      ],
    },
    socialLinks: [{ icon: 'github', link: meta.repository }],
    footer: {
      message: `${meta.name} v${meta.version} · ${meta.release_date} · MIT · Not financial, legal or tax advice.`,
      copyright: `<a href="/guide/privacy">Privacy</a> · <a href="${meta.homepage}/#contact">Contact</a> · <a href="${meta.homepage}">fundadmin.dev</a>`,
    },
  },
})
