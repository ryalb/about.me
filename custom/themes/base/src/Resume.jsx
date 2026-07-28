import React from 'react';
import styled from 'styled-components';
import { Section as CoreSection, DateRange, ContactInfo } from '@jsonresume/core';
import { colors, fonts, type, space, layout } from './tokens.js';

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
  padding-bottom: 28px;
  // border-bottom: 2px solid ${colors.rule};
`;

const Name = styled.h1`
  font-size: ${type.name};
  font-weight: 300;
  color: ${colors.ink};
  margin: 0 0 10px 0;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  text-align: center;
`;

const Label = styled.div`
  font-size: ${type.meta};
  color: ${colors.subtle};
  margin-bottom: 20px;
  font-weight: 400;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-align: center;
`;

const StyledContactInfo = styled(ContactInfo)`
  font-size: ${type.body};
  color: ${colors.muted};

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

  span {
    color: ${colors.faint};
  }
`;

const Summary = styled.p`
  font-size: ${type.summary};
  line-height: 1.8;
  color: ${colors.body};
  margin: 20px 0 0 0;
  font-weight: 300;
`;

const SectionTitle = styled.h2`
  font-size: ${type.sectionTitle};
  font-weight: 500;
  color: ${colors.muted};
  margin: ${space.sectionGap} 0 26px 0;
  letter-spacing: 3px;
  text-transform: uppercase;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: -10px;
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
  padding: 16px 0;

  @media print {
    break-inside: avoid;
    page-break-inside: avoid;
  }
`;

const ItemHeader = styled.div`
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 24px;
  margin-bottom: 10px;
  align-items: baseline;

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
    gap: 6px;
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
  letter-spacing: 0.5px;

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
  margin-top: 4px;

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
  letter-spacing: 0.5px;
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
  margin: 10px 0;
  color: ${colors.muted};
  line-height: 1.8;
  font-size: ${type.body};
  font-weight: 300;
`;

const Highlights = styled.ul`
  margin: 10px 0 0 0;
  padding-left: 20px;
  list-style-type: none;

  li {
    margin: 7px 0;
    color: ${colors.muted};
    line-height: 1.75;
    font-size: ${type.body};
    font-weight: 300;
    position: relative;

    &::before {
      content: '—';
      position: absolute;
      left: -20px;
      color: ${colors.subtle};
    }
  }
`;

const KeywordRow = styled.div`
  margin-top: 10px;
  font-size: ${type.small};
  color: ${colors.subtle};
  font-weight: 300;
  letter-spacing: 0.3px;
`;

/* ────────────────────────────────────────────────────────────────────────
   Cards (skills, languages, interests)
   ──────────────────────────────────────────────────────────────────────── */

const CardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 22px;
`;

const Card = styled.div`
  padding: 20px;
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
  margin: 0 0 8px 0;
  letter-spacing: 1px;
  text-transform: uppercase;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
`;

const CardLevel = styled.span`
  font-size: ${type.small};
  font-weight: 300;
  color: ${colors.faint};
  letter-spacing: 0.5px;
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
  } = resume;

  return (
    <Layout>
      <Header>
        <Name>{basics.name}</Name>
        {basics.label && <Label>{basics.label}</Label>}
        <StyledContactInfo basics={basics} />
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
                  <DateRange startDate={job.startDate} endDate={job.endDate} />
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
                      endDate={edu.endDate}
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
                      endDate={project.endDate}
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
                    <DateRange startDate={vol.startDate} endDate={vol.endDate} />
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
                  {award.title && <ItemTitle>{award.title}</ItemTitle>}
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
