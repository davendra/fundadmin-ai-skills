import { defineConfig } from 'vitepress'
// Written by tools/build_plugin.py in davendra/fundadmin-ai from the plugin
// metadata and skill registry. It is the only thing this config knows about
// the plugin, so version, counts and the commands sidebar cannot drift.
import meta from './meta.json'

const site = meta.docs
const categories = meta.categories as { name: string; slug: string; count: number }[]

export default defineConfig({
  title: 'FundAdmin AI Help',
  description: `User manual for the ${meta.name} plugin: ${meta.skill_count} fund administration skills. Install in Claude Code, ChatGPT desktop, ChatGPT Work or Codex; qualification varies by host.`,
  lang: 'en-GB',
  cleanUrls: true,
  ignoreDeadLinks: false,
  // The published repository is one squashed commit per release, so git dates
  // would all be the release date. The footer carries the version instead.
  lastUpdated: false,
  srcExclude: ['DEPLOY.md', 'README.md'],
  sitemap: { hostname: site },
  head: [
    ['link', { rel: 'icon', href: '/fundadmin-ai-favicon.svg' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'FundAdmin AI Help' }],
    ['meta', { property: 'og:description', content: `Install and use the ${meta.name} plugin: ${meta.skill_count} fund administration skills and ${meta.agent_count} LPA-review agents. Claude Code is the primary target; ChatGPT and other hosts remain experimental.` }],
    ['meta', { property: 'og:image', content: `${site}/images/fundadmin-ai-mark.png` }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'twitter:image', content: `${site}/images/fundadmin-ai-mark.png` }],
  ],
  transformHead({ pageData }) {
    const path = pageData.relativePath.replace(/index\.md$/, '').replace(/\.md$/, '')
    const url = `${site}/${path}`
    const title = pageData.title === 'FundAdmin AI Help' ? pageData.title : `${pageData.title} | FundAdmin AI Help`
    return [
      ['link', { rel: 'canonical', href: url }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:title', content: title }],
      ['meta', { name: 'twitter:title', content: title }],
    ]
  },
  themeConfig: {
    logo: { src: '/images/fundadmin-ai-mark.png', alt: '' },
    siteTitle: 'FundAdmin AI',
    search: { provider: 'local' },
    nav: [
      { text: 'Guide', link: '/guide/install' },
      { text: 'Commands', link: '/commands/' },
      { text: 'Agents', link: '/agents' },
      { text: 'Examples', link: '/guide/examples' },
      { text: 'Contact', link: 'https://fundadmin.dev/#contact' },
      { text: `v${meta.version}`, link: '/guide/release' },
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
            { text: 'Worked examples', link: '/guide/examples' },
            { text: 'Release and host support', link: '/guide/release' },
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
        { text: 'Agents', items: [{ text: `The ${meta.agent_count} LPA-review agents`, link: '/agents' }] },
      ],
    },
    socialLinks: [{ icon: 'github', link: meta.repository }],
    footer: {
      message: `Plugin v${meta.version} · Released ${meta.release_date} · Help updated 16 October 2026 · MIT<br>Not financial, legal or tax advice. Qualified human review required.`,
      copyright: `<a href="/guide/privacy">Privacy</a> · <a href="${meta.homepage}/#contact">Contact</a> · <a href="${meta.homepage}">fundadmin.dev</a>`,
    },
  },
})
