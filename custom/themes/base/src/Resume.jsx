import React from 'react';
import styled from 'styled-components';
import { Section as CoreSection } from '@jsonresume/core';
import { colors, fonts, type, space, layout, scale } from './tokens.js';
import { Icon, networkIcon } from './Icon.jsx';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join as pathJoin } from 'path';

const MONTHS_PT = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  if (dateStr.length === 4 && /^\d{4}$/.test(dateStr)) {
    return dateStr;
  }
  const parts = dateStr.split('-');
  const year = parts[0];
  if (parts.length < 2) return dateStr;
  const month = parseInt(parts[1], 10);
  if (month >= 1 && month <= 12) {
    return `${MONTHS_PT[month - 1]}/${year}`;
  }
  return dateStr;
};

const formatDateRange = (start, end, present) => {
  const startStr = formatDate(start);
  const endStr = end ? formatDate(end) : (startStr ? present : '');
  if (startStr && endStr) {
    return `${startStr} - ${endStr}`;
  }
  return startStr || endStr || '';
};

/* ────────────────────────────────────────────────────────────────────────
   Locale loader

   Strings are loaded from ``locales/<tag>.json`` alongside this theme.
   Fallback order: full BCP 47 tag → bare language subtag → English.
   ──────────────────────────────────────────────────────────────────────── */

const __dirname = dirname(fileURLToPath(import.meta.url));
const LOCALES_DIR = pathJoin(__dirname, '..', 'locales');
const _localeCache = {};

const readTable = (baseDir, name) => {
  try {
    return JSON.parse(readFileSync(pathJoin(baseDir, `${name}.json`), 'utf-8'));
  } catch {
    return null;
  }
};

const mergeTables = (base, override) => {
  const out = { ...base };
  for (const [key, value] of Object.entries(override)) {
    const plain = (v) => v && typeof v === 'object' && !Array.isArray(v);
    out[key] = plain(value) && plain(out[key]) ? mergeTables(out[key], value) : value;
  }
  return out;
};

/* Overlay the requested table on English so a missing key never leaves a
   blank label or falls back to a hard-coded string. */
const loadLocale = (tag, baseDir = LOCALES_DIR) => {
  const cacheKey = `${baseDir}:${tag}`;
  if (_localeCache[cacheKey]) return _localeCache[cacheKey];
  const english = readTable(baseDir, 'en') || {};
  let table = english;
  for (const c of new Set([tag, tag.split('-')[0].toLowerCase()])) {
    if (c === 'en') break;
    const found = readTable(baseDir, c);
    if (found) {
      table = mergeTables(english, found);
      break;
    }
  }
  _localeCache[cacheKey] = table;
  return table;
};

/* ────────────────────────────────────────────────────────────────────────
   Section wrapper

   @jsonresume/core's <Section> hard-codes `page-break-inside: avoid` in a
   print media query.  Applied to a whole section that is taller than one
   page (e.g. Experience) it is unsatisfiable, so the renderer pushes the
   entire section to the next page — leaving the first page nearly empty
   and inflating the page count.

   Override it back to `auto` so sections may break internally; the finer
   -grained rules below (entry headings, bullets, cards) do the real work.
   ──────────────────────────────────────────────────────────────────────── */

const Section = styled(CoreSection)`
  @media print {
    break-inside: auto;
    page-break-inside: auto;
  }
`;

/* ────────────────────────────────────────────────────────────────────────
   Layout
   ──────────────────────────────────────────────────────────────────────── */

const Layout = styled.div`
  max-width: ${layout.maxWidth};
  margin: 0 auto;
  padding: ${space.pagePaddingY} ${space.pagePaddingX};
  background: ${colors.page};
  font-family: ${fonts.sans};
  color: ${colors.body};
  line-height: 1.6;

  @media print {
    padding: ${layout.printPagePaddingY} ${layout.printPagePaddingX};
    background: ${colors.surface};
    max-width: none;
  }
`;

const Header = styled.header`
  margin-bottom: ${space.headerGap};
  padding-bottom: ${scale(28)};
  // border-bottom: 2px solid ${colors.rule};
`;

const Name = styled.h1`
  font-size: ${type.name};
  font-weight: ${fonts.weights.bold};
  color: ${colors.ink};
  margin: 0 0 ${scale(10)} 0;
  letter-spacing: ${scale(0.5)};
  text-transform: uppercase;
  text-align: center;
`;

const Label = styled.div`
  font-size: ${type.meta};
  color: ${colors.subtle};
  margin-bottom: ${scale(20)};
  font-weight: 400;
  letter-spacing: ${scale(2)};
  text-transform: uppercase;
  text-align: center;
`;

/* ────────────────────────────────────────────────────────────────────────
   Contact line

   Replaces @jsonresume/core's <ContactInfo>, which renders text-only items
   and drops a profile when `network` is missing.  This version prefixes each
   item with an inline MDI icon (see Icon.jsx) and keeps the username visible
   alongside the network name.
   ──────────────────────────────────────────────────────────────────────── */

/* Inline layout, not flex: WeasyPrint's flexbox support does not honour
   align-items reliably, which left the separators floating above the text
   baseline in PDF output.  Inline-block + vertical-align is exact in both
   browsers and WeasyPrint. */
const ContactRow = styled.div`
  text-align: center;
  font-size: ${type.body};
  color: ${colors.muted};
  line-height: 1.9;

  a {
    font-size: ${type.body};
    color: ${colors.muted};
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;

    &:hover {
      border-bottom-color: ${colors.muted};
    }
  }
`;

const ContactItem = styled.span`
  white-space: nowrap;
`;

/* Drawn as a CSS circle rather than the '•' character: the theme font
   (IosevkaTermSlab, a terminal face) places U+2022 high in the em box, so a
   text bullet floats above the contact line instead of centring on it. */
const Separator = styled.span`
  display: inline-block;
  width: ${scale(3)};
  height: ${scale(3)};
  margin: 0 ${scale(9)};
  border-radius: 50%;
  background: ${colors.faint};
  vertical-align: 0.25em;
`;

/* Profile display text — prefer the URL with its scheme and trailing slash
   removed ("linkedin.com/in/ryalb").  PDF text extraction and ATS parsers read
   the rendered text, never the href, so a bare username leaves no route back
   to the profile.  Mirrors profile_display() in resume_generator/contact.py. */
const profileDisplay = (profile = {}) => {
  const url = (profile.url || '').trim();
  if (url) {
    return url.replace(/^[a-z][a-z0-9+.-]*:\/\//i, '').replace(/\/$/, '');
  }
  const network = (profile.network || '').trim();
  const username = (profile.username || '').trim();
  if (network && username) return `${network}: ${username}`;
  return username || network;
};

const ContactInfo = ({ basics = {}, labels = {} }) => {
  const { email, phone, url, location, profiles = [] } = basics;
  const items = [];

  if (email) {
    items.push(
      <ContactItem key="email">
        <Icon name="email" />
        <a href={`mailto:${email}`} aria-label={labels.email}>
          {email}
        </a>
      </ContactItem>
    );
  }

  if (phone) {
    items.push(
      <ContactItem key="phone">
        <Icon name="phone" />
        <a href={`tel:${phone.replace(/\s+/g, '')}`} aria-label={labels.phone}>
          {phone}
        </a>
      </ContactItem>
    );
  }

  const locationStr = location
    ? [location.city, location.region, location.countryCode]
        .filter(Boolean)
        .join(', ')
    : '';
  if (locationStr) {
    items.push(
      <ContactItem key="location" aria-label={labels.location}>
        <Icon name="location" />
        {locationStr}
      </ContactItem>
    );
  }

  if (url) {
    items.push(
      <ContactItem key="url">
        <Icon name="website" />
        <a href={url} target="_blank" rel="noopener noreferrer" aria-label={labels.website}>
          {url.replace(/^https?:\/\//, '').replace(/\/$/, '')}
        </a>
      </ContactItem>
    );
  }

  profiles.forEach((profile, index) => {
    const text = profileDisplay(profile);
    if (!text) return;
    items.push(
      <ContactItem key={`profile-${index}`}>
        <Icon name={networkIcon(profile.network)} />
        {profile.url ? (
          <a
            href={profile.url}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={profile.network || labels.profile}
          >
            {text}
          </a>
        ) : (
          text
        )}
      </ContactItem>
    );
  });

  if (items.length === 0) return null;
  return (
    <ContactRow className="resume-contact">
      {items.map((item, index) => (
        <React.Fragment key={item.key ?? index}>
          {index > 0 && <Separator aria-hidden="true" />}
          {item}
        </React.Fragment>
      ))}
    </ContactRow>
  );
};

const Summary = styled.p`
  font-size: ${type.summary};
  line-height: 1.8;
  color: ${colors.body};
  margin: ${scale(20)} 0 0 0;
  font-weight: 300;
`;

const SectionTitle = styled.h2`
  font-size: ${type.sectionTitle};
  font-weight: 500;
  color: ${colors.muted};
  margin: ${space.sectionGap} 0 ${scale(26)} 0;
  letter-spacing: ${scale(3)};
  text-transform: uppercase;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: -${scale(10)};
    left: 0;
    right: 0;
    height: 1px;
    background: ${colors.rule};
  }

  /* Never leave a section heading stranded at the foot of a page. */
  @media print {
    break-after: avoid;
    page-break-after: avoid;
  }
`;

/* ────────────────────────────────────────────────────────────────────────
   Entries
   ──────────────────────────────────────────────────────────────────────── */

const Item = styled.div`
  padding: ${space.itemGap} 0;
  border-bottom: 1px solid ${colors.hairline};

  &:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  /*
   * Deliberately NOT using break-inside: avoid here.
   *
   * Work entries are tall (summary + several highlights).  Forbidding an
   * internal break means a tall entry that doesn't fit in the remaining
   * space gets pushed wholesale to the next page, leaving large gaps and
   * adding ~2 pages across a full resume.  Splitting a long entry between
   * pages is fine to read; orphans/widows in index.jsx prevent the ugly
   * cases (a single stranded line).
   *
   * Instead, just keep the entry's own heading with the text that follows it.
   */
  @media print {
    h3 {
      break-after: avoid;
      page-break-after: avoid;
    }
  }
`;

/** Short, atomic entries that genuinely should never split. */
const CompactItem = styled(Item)`
  padding: ${scale(16)} 0;

  @media print {
    break-inside: avoid;
    page-break-inside: avoid;
  }
`;

const ItemHeader = styled.div`
  display: grid;
  grid-template-columns: 1fr auto;
  gap: ${scale(24)};
  margin-bottom: ${scale(10)};
  align-items: baseline;

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
    gap: ${scale(6)};
  }

  /*
   * Never split the title/company/date block itself.
   *
   * break-after is scoped to headers that actually have a body after them.
   * On an entry whose header is its only child (an education entry with no
   * summary and no courses) the rule has no next sibling inside the Item, so
   * it propagates to the following in-flow box -- the next SectionTitle,
   * which carries its own break-after: avoid -- and the chain drags that
   * heading and its whole section to the next page, stranding most of a page
   * of whitespace.
   */
  @media print {
    break-inside: avoid;
    page-break-inside: avoid;

    &:not(:last-child) {
      break-after: avoid;
      page-break-after: avoid;
    }
  }
`;

const ItemTitle = styled.h3`
  font-size: ${type.itemTitle};
  font-weight: 400;
  color: ${colors.ink};
  margin: 0;
  letter-spacing: ${scale(0.5)};

  a {
    color: inherit;
    text-decoration: none;
    border-bottom: 1px solid ${colors.rule};

    &:hover {
      border-bottom-color: ${colors.ink};
    }
  }
`;

const ItemSubtitle = styled.div`
  font-size: ${type.itemSubtitle};
  color: ${colors.subtle};
  font-weight: 300;
  margin-top: ${scale(4)};

  a {
    color: inherit;
    text-decoration: none;
    border-bottom: 1px solid transparent;

    &:hover {
      border-bottom-color: ${colors.subtle};
    }
  }
`;

const MetaText = styled.div`
  font-size: ${type.meta};
  color: ${colors.faint};
  font-weight: 300;
  white-space: nowrap;
  letter-spacing: ${scale(0.5)};
  text-align: right;
`;

const Location = styled.span`
  color: ${colors.faint};
  font-size: ${type.meta};

  &::before {
    content: ' · ';
  }
`;

const BodyText = styled.p`
  margin: ${scale(10)} 0;
  color: ${colors.muted};
  line-height: 1.8;
  font-size: ${type.body};
  font-weight: 300;
`;

const Highlights = styled.ul`
  margin: ${scale(10)} 0 0 0;
  padding-left: ${scale(20)};
  list-style-type: none;

  li {
    margin: ${scale(7)} 0;
    color: ${colors.muted};
    line-height: 1.75;
    font-size: ${type.body};
    font-weight: 300;
    position: relative;

    &::before {
      content: '—';
      position: absolute;
      left: -${scale(20)};
      color: ${colors.subtle};
    }
  }
`;

const KeywordRow = styled.div`
  margin-top: ${scale(10)};
  font-size: ${type.small};
  color: ${colors.subtle};
  font-weight: 300;
  letter-spacing: ${scale(0.3)};
`;

/* ────────────────────────────────────────────────────────────────────────
   Cards (skills, languages, interests)
   ──────────────────────────────────────────────────────────────────────── */

const CardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(${scale(260)}, 1fr));
  gap: ${scale(16)};
  margin-top: ${scale(22)};

  /* WeasyPrint implements CSS Grid but does not resolve auto-fill / auto-fit
     repeat() into a track count, so every card was laid out in a single
     full-width column in the PDF while the browser showed two.  At A4 minus
     page margins the screen rule resolves to two tracks anyway, so state that
     explicitly for print to keep PDF and HTML identical. */
  /* Print goes single-column on purpose.  The two-column grid interleaves
     under plain text extraction -- the form most ATS parsers use -- splitting
     multi-word keywords (Strawberry GraphQL, Tailwind CSS, Multi-arch builds)
     and detaching each proficiency level from its category.  One column costs
     no pages and keeps every keyword intact. */
  @media print {
    grid-template-columns: 1fr;
  }
`;

const Card = styled.div`
  padding: ${scale(10)};
  background: ${colors.surface};
  border: 1px solid ${colors.rule};
  border-radius: 2px;

  @media print {
    break-inside: avoid;
    page-break-inside: avoid;
  }
`;

const CardTitle = styled.h4`
  font-size: ${type.body};
  font-weight: 500;
  color: ${colors.ink};
  margin: 0 0 ${scale(8)} 0;
  letter-spacing: ${scale(1)};
  text-transform: uppercase;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: ${scale(8)};
`;

const CardLevel = styled.span`
  font-size: ${type.small};
  font-weight: 300;
  color: ${colors.faint};
  letter-spacing: ${scale(0.5)};
  text-transform: none;
`;

const CardBody = styled.div`
  font-size: ${type.meta};
  color: ${colors.subtle};
  line-height: 1.7;
  font-weight: 300;
`;

/* ────────────────────────────────────────────────────────────────────────
   Helpers
   ──────────────────────────────────────────────────────────────────────── */

/** Render a title, wrapped in a link when a url is present. */
const MaybeLink = ({ url, children }) =>
  url ? (
    <a href={url} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  ) : (
    children
  );

/** Join non-empty parts with a separator. */
const join = (parts, sep = ' · ') => parts.filter(Boolean).join(sep);

/* ────────────────────────────────────────────────────────────────────────
   Ongoing entries

   JSON Resume marks work that hasn't finished by omitting `endDate`.
   @jsonresume/utils treats an *undefined* endDate as a single point in time
   (correct for award/certificate dates) and only appends the "Present" label
   when endDate is explicitly `null` — so every date *range* passes
   `endDate ?? null` to opt into the label.

    The label is passed as `presentLabel` so it comes from our locale JSON;
    `locale` localises the month names to the document language.
    ──────────────────────────────────────────────────────────────────────── */

/* Disclosure for a date-trimmed work history.  Without it a reader cannot tell
   a filtered résumé from a short career.  The strings come from the locale
   JSON loaded above, keeping them in step with the tables in
   resume_generator/locales/. */

const workCutoffNotice = (meta = {}, localeData) => {
  const count = meta.filtered?.hidden?.work ?? 0;
  if (!count) return null;
  const notices = localeData?.cutoff_notice || {};
  const template = notices[count === 1 ? 'one' : 'many'];
  if (!template) return null;
  return template
    .replace('{count}', String(count))
    .replace('{date}', meta.filtered?.cutDate ?? '');
};

const CutoffNotice = styled.p`
  font-size: ${type.meta};
  font-style: italic;
  text-align: center;
  color: ${colors.faint};
  margin: ${scale(10)} 0 0 0;
`;

/* ────────────────────────────────────────────────────────────────────────
   Resume
   ──────────────────────────────────────────────────────────────────────── */

function Resume({ resume, themeDir }) {
  const {
    basics = {},
    meta = {},
  } = resume;

  const localeBaseDir = themeDir ? pathJoin(themeDir, 'locales') : LOCALES_DIR;
  const localeData = React.useMemo(() => loadLocale(meta.language || 'en-US', localeBaseDir), [meta.language, localeBaseDir]);
  const presentLabel = localeData.present;
  const labels = localeData.section || {};
  const cutoffNotice = workCutoffNotice(meta, localeData);

  return (
    <Layout>
      <Header>
        <Name>{basics.name}</Name>
        {basics.label && <Label>{basics.label}</Label>}
        <ContactInfo basics={basics} labels={localeData.contact} />
        {basics.summary && <Summary>{basics.summary}</Summary>}
      </Header>

      {Object.entries(resume).map(([key, value]) => {
        if (key === 'basics' || key === 'meta' || key === '$schema') return null;
        if (!Array.isArray(value) || value.length === 0) return null;

        if (key === 'skills') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.skills}</SectionTitle>
              <CardGrid>
                {value.map((skill, i) => (
                  <Card key={i}>
                    {skill.name && (
                      <CardTitle>
                        <span>{skill.name}</span>
                        {skill.level && <CardLevel>{skill.level}</CardLevel>}
                      </CardTitle>
                    )}
                    {skill.keywords?.length > 0 && (
                      <CardBody>{skill.keywords.join(', ')}</CardBody>
                    )}
                  </Card>
                ))}
              </CardGrid>
            </Section>
          );
        }

        if (key === 'work') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.work}</SectionTitle>
              {value.map((job, i) => (
                <Item key={i}>
                  <ItemHeader>
                    <div>
                      {job.position && <ItemTitle>{job.position}</ItemTitle>}
                      {job.name && (
                        <ItemSubtitle>
                          <MaybeLink url={job.url}>{job.name}</MaybeLink>
                          {job.location && <Location>{job.location}</Location>}
                        </ItemSubtitle>
                      )}
                    </div>
                    <MetaText>
                      {formatDateRange(job.startDate, job.endDate ?? null, presentLabel)}
                    </MetaText>
                  </ItemHeader>
                  {job.summary && <BodyText>{job.summary}</BodyText>}
                  {job.highlights?.length > 0 && (
                    <Highlights>
                      {job.highlights.map((h, j) => (
                        <li key={j}>{h}</li>
                      ))}
                    </Highlights>
                  )}
                </Item>
              ))}
              {cutoffNotice && <CutoffNotice>{cutoffNotice}</CutoffNotice>}
            </Section>
          );
        }

        if (key === 'projects') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.projects}</SectionTitle>
              {value.map((project, i) => (
                <Item key={i}>
                  <ItemHeader>
                    <div>
                      {project.name && (
                        <ItemTitle>
                          <MaybeLink url={project.url}>{project.name}</MaybeLink>
                        </ItemTitle>
                      )}
                      {(project.type || project.entity || project.roles?.length) && (
                        <ItemSubtitle>
                          {join([
                            project.type,
                            project.entity,
                            project.roles?.join(', '),
                          ])}
                        </ItemSubtitle>
                      )}
                    </div>
                    {(project.startDate || project.endDate) && (
                      <MetaText>
                        {formatDateRange(project.startDate, project.endDate ?? null, presentLabel)}
                      </MetaText>
                    )}
                  </ItemHeader>
                  {project.description && <BodyText>{project.description}</BodyText>}
                  {project.highlights?.length > 0 && (
                    <Highlights>
                      {project.highlights.map((h, j) => (
                        <li key={j}>{h}</li>
                      ))}
                    </Highlights>
                  )}
                  {project.keywords?.length > 0 && (
                    <KeywordRow>{project.keywords.join(' · ')}</KeywordRow>
                  )}
                </Item>
              ))}
            </Section>
          );
        }

        if (key === 'volunteer') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.volunteer}</SectionTitle>
              {value.map((vol, i) => (
                <Item key={i}>
                  <ItemHeader>
                    <div>
                      {vol.position && <ItemTitle>{vol.position}</ItemTitle>}
                      {vol.organization && (
                        <ItemSubtitle>
                          <MaybeLink url={vol.url}>{vol.organization}</MaybeLink>
                        </ItemSubtitle>
                      )}
                    </div>
                    {(vol.startDate || vol.endDate) && (
                      <MetaText>
                        {formatDateRange(vol.startDate, vol.endDate ?? null, presentLabel)}
                      </MetaText>
                    )}
                  </ItemHeader>
                  {vol.summary && <BodyText>{vol.summary}</BodyText>}
                  {vol.highlights?.length > 0 && (
                    <Highlights>
                      {vol.highlights.map((h, j) => (
                        <li key={j}>{h}</li>
                      ))}
                    </Highlights>
                  )}
                </Item>
              ))}
            </Section>
          );
        }

        if (key === 'education') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.education}</SectionTitle>
              {value.map((edu, i) => (
                <Item key={i}>
                  <ItemHeader>
                    <div>
                      {edu.institution && (
                        <ItemTitle>
                          <MaybeLink url={edu.url}>{edu.institution}</MaybeLink>
                        </ItemTitle>
                      )}
                       {(edu.studyType || edu.area) && (
                        <ItemSubtitle>
                          {join(
                            [
                              edu.studyType && edu.area
                                ? `${edu.studyType} ${localeData.education?.in} ${edu.area}`
                                : edu.studyType || edu.area,
                              edu.score && `${localeData.education?.score} ${edu.score}`,
                              edu.workload && `${localeData.education?.workload} ${edu.workload}`,
                            ],
                            ' · '
                          )}
                        </ItemSubtitle>
                      )}
                    </div>
                    {(edu.startDate || edu.endDate) && (
                      <MetaText>
                        {formatDateRange(edu.startDate, edu.endDate ?? null, presentLabel)}
                      </MetaText>
                    )}
                  </ItemHeader>
                  {edu.summary && <BodyText>{edu.summary}</BodyText>}
                  {edu.courses?.length > 0 && (
                    <KeywordRow>{edu.courses.join(' · ')}</KeywordRow>
                  )}
                </Item>
              ))}
            </Section>
          );
        }

        if (key === 'certificates') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.certificates}</SectionTitle>
              {value.map((cert, i) => (
                <CompactItem key={i}>
                  <ItemHeader>
                    <div>
                      {cert.name && (
                        <ItemTitle>
                          <MaybeLink url={cert.url}>{cert.name}</MaybeLink>
                        </ItemTitle>
                      )}
                      {cert.issuer && <ItemSubtitle>{cert.issuer}</ItemSubtitle>}
                    </div>
                    {cert.date && <MetaText>{formatDate(cert.date)}</MetaText>}
                  </ItemHeader>
                </CompactItem>
              ))}
            </Section>
          );
        }

        if (key === 'publications') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.publications}</SectionTitle>
              {value.map((pub, i) => (
                <Item key={i}>
                  <ItemHeader>
                    <div>
                      {pub.name && (
                        <ItemTitle>
                          <MaybeLink url={pub.url}>{pub.name}</MaybeLink>
                        </ItemTitle>
                      )}
                      {pub.publisher && (
                        <ItemSubtitle>{pub.publisher}</ItemSubtitle>
                      )}
                    </div>
                    {pub.releaseDate && <MetaText>{formatDate(pub.releaseDate)}</MetaText>}
                  </ItemHeader>
                  {pub.summary && <BodyText>{pub.summary}</BodyText>}
                </Item>
              ))}
            </Section>
          );
        }

        if (key === 'awards') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.awards}</SectionTitle>
              {value.map((award, i) => (
                <Item key={i}>
                  <ItemHeader>
                    <div>
                      {award.title && (
                        <ItemTitle>
                          <MaybeLink url={award.url}>{award.title}</MaybeLink>
                        </ItemTitle>
                      )}
                      {award.awarder && <ItemSubtitle>{award.awarder}</ItemSubtitle>}
                    </div>
                    {award.date && <MetaText>{formatDate(award.date)}</MetaText>}
                  </ItemHeader>
                  {award.summary && <BodyText>{award.summary}</BodyText>}
                </Item>
              ))}
            </Section>
          );
        }

        if (key === 'languages') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.languages}</SectionTitle>
              <CardGrid>
                {value.map((lang, i) => (
                  <Card key={i}>
                    {lang.language && (
                      <CardTitle>
                        <span>{lang.language}</span>
                      </CardTitle>
                    )}
                    {lang.fluency && <CardBody>{lang.fluency}</CardBody>}
                  </Card>
                ))}
              </CardGrid>
            </Section>
          );
        }

        if (key === 'interests') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.interests}</SectionTitle>
              <CardGrid>
                {value.map((interest, i) => (
                  <Card key={i}>
                    {interest.name && (
                      <CardTitle>
                        <span>{interest.name}</span>
                      </CardTitle>
                    )}
                    {interest.keywords?.length > 0 && (
                      <CardBody>{interest.keywords.join(', ')}</CardBody>
                    )}
                  </Card>
                ))}
              </CardGrid>
            </Section>
          );
        }

        if (key === 'references') {
          return (
            <Section key={key}>
              <SectionTitle>{labels.references}</SectionTitle>
              {value.map((ref, i) => (
                <Item key={i}>
                  {ref.name && <ItemTitle>{ref.name}</ItemTitle>}
                  {ref.reference && <BodyText>{ref.reference}</BodyText>}
                </Item>
              ))}
            </Section>
          );
        }

        return null;
      })}
    </Layout>
  );
}

export default Resume;
