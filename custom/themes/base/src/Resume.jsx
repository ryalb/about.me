import React from 'react';
import styled from 'styled-components';
import { Section as CoreSection, DateRange } from '@jsonresume/core';
import { colors, fonts, type, space, layout, scale } from './tokens.js';
import { Icon, networkIcon } from './Icon.jsx';

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

const ContactInfo = ({ basics = {} }) => {
  const { email, phone, url, location, profiles = [] } = basics;
  const items = [];

  if (email) {
    items.push(
      <ContactItem key="email">
        <Icon name="email" />
        <a href={`mailto:${email}`} aria-label="Email">
          {email}
        </a>
      </ContactItem>
    );
  }

  if (phone) {
    items.push(
      <ContactItem key="phone">
        <Icon name="phone" />
        <a href={`tel:${phone.replace(/\s+/g, '')}`} aria-label="Phone">
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
      <ContactItem key="location" aria-label="Location">
        <Icon name="location" />
        {locationStr}
      </ContactItem>
    );
  }

  if (url) {
    items.push(
      <ContactItem key="url">
        <Icon name="website" />
        <a href={url} target="_blank" rel="noopener noreferrer" aria-label="Website">
          {url.replace(/^https?:\/\//, '').replace(/\/$/, '')}
        </a>
      </ContactItem>
    );
  }

  profiles.forEach((profile, index) => {
    const text = profile.username || profile.network || profile.url;
    if (!text) return;
    items.push(
      <ContactItem key={`profile-${index}`}>
        <Icon name={networkIcon(profile.network)} />
        {profile.url ? (
          <a
            href={profile.url}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={profile.network || 'Profile'}
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

  /* Never split the title/company/date block itself. */
  @media print {
    break-inside: avoid;
    page-break-inside: avoid;
    break-after: avoid;
    page-break-after: avoid;
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
  @media print {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
`;

const Card = styled.div`
  padding: ${scale(20)};
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

   The label is passed as `presentLabel` rather than through DateRange's
   `locale` prop: `locale` would also localise month names, changing every
   date in the document.  Keep this table in step with
   `resume_generator/i18n.py`, which resolves the same label for md/txt/docx.
   ──────────────────────────────────────────────────────────────────────── */

const PRESENT_LABELS = {
  en: 'Present',
  pt: 'Presente',
  es: 'Presente',
  fr: 'Présent',
  it: 'Presente',
  de: 'Heute',
};

const presentLabelFor = (language) => {
  const tag = (language || 'en-US').trim();
  return (
    PRESENT_LABELS[tag] ||
    PRESENT_LABELS[tag.split('-')[0].toLowerCase()] ||
    PRESENT_LABELS.en
  );
};

/* ────────────────────────────────────────────────────────────────────────
   Resume
   ──────────────────────────────────────────────────────────────────────── */

function Resume({ resume }) {
  const {
    basics = {},
    work = [],
    education = [],
    skills = [],
    projects = [],
    volunteer = [],
    awards = [],
    certificates = [],
    publications = [],
    languages = [],
    interests = [],
    references = [],
    meta = {},
  } = resume;

  const presentLabel = presentLabelFor(meta.language);

  return (
    <Layout>
      <Header>
        <Name>{basics.name}</Name>
        {basics.label && <Label>{basics.label}</Label>}
        <ContactInfo basics={basics} />
        {basics.summary && <Summary>{basics.summary}</Summary>}
      </Header>

      {work.length > 0 && (
        <Section>
          <SectionTitle>Experience</SectionTitle>
          {work.map((job, i) => (
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
                  <DateRange
                    startDate={job.startDate}
                    endDate={job.endDate ?? null}
                    presentLabel={presentLabel}
                  />
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
        </Section>
      )}

      {skills.length > 0 && (
        <Section>
          <SectionTitle>Skills</SectionTitle>
          <CardGrid>
            {skills.map((skill, i) => (
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
      )}

      {education.length > 0 && (
        <Section>
          <SectionTitle>Education</SectionTitle>
          {education.map((edu, i) => (
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
                            ? `${edu.studyType} in ${edu.area}`
                            : edu.studyType || edu.area,
                          edu.score && `Score: ${edu.score}`,
                        ],
                        ' · '
                      )}
                    </ItemSubtitle>
                  )}
                </div>
                {(edu.startDate || edu.endDate) && (
                  <MetaText>
                    <DateRange
                      startDate={edu.startDate}
                      endDate={edu.endDate ?? null}
                      presentLabel={presentLabel}
                    />
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
      )}

      {projects.length > 0 && (
        <Section>
          <SectionTitle>Projects</SectionTitle>
          {projects.map((project, i) => (
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
                    <DateRange
                      startDate={project.startDate}
                      endDate={project.endDate ?? null}
                      presentLabel={presentLabel}
                    />
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
      )}

      {volunteer.length > 0 && (
        <Section>
          <SectionTitle>Volunteer</SectionTitle>
          {volunteer.map((vol, i) => (
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
                    <DateRange
                      startDate={vol.startDate}
                      endDate={vol.endDate ?? null}
                      presentLabel={presentLabel}
                    />
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
      )}

      {publications.length > 0 && (
        <Section>
          <SectionTitle>Publications</SectionTitle>
          {publications.map((pub, i) => (
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
                {pub.releaseDate && <MetaText>{pub.releaseDate}</MetaText>}
              </ItemHeader>
              {pub.summary && <BodyText>{pub.summary}</BodyText>}
            </Item>
          ))}
        </Section>
      )}

      {awards.length > 0 && (
        <Section>
          <SectionTitle>Awards</SectionTitle>
          {awards.map((award, i) => (
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
                {award.date && <MetaText>{award.date}</MetaText>}
              </ItemHeader>
              {award.summary && <BodyText>{award.summary}</BodyText>}
            </Item>
          ))}
        </Section>
      )}

      {certificates.length > 0 && (
        <Section>
          <SectionTitle>Certificates</SectionTitle>
          {certificates.map((cert, i) => (
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
                {cert.date && <MetaText>{cert.date}</MetaText>}
              </ItemHeader>
            </CompactItem>
          ))}
        </Section>
      )}

      {languages.length > 0 && (
        <Section>
          <SectionTitle>Languages</SectionTitle>
          <CardGrid>
            {languages.map((lang, i) => (
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
      )}

      {interests.length > 0 && (
        <Section>
          <SectionTitle>Interests</SectionTitle>
          <CardGrid>
            {interests.map((interest, i) => (
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
      )}

      {references.length > 0 && (
        <Section>
          <SectionTitle>References</SectionTitle>
          {references.map((ref, i) => (
            <Item key={i}>
              {ref.name && <ItemTitle>{ref.name}</ItemTitle>}
              {ref.reference && <BodyText>{ref.reference}</BodyText>}
            </Item>
          ))}
        </Section>
      )}
    </Layout>
  );
}

export default Resume;
