const fs = require('fs');

const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const changelog = fs.readFileSync('CHANGELOG.md', 'utf8');
const readme = fs.readFileSync('README.md', 'utf8');

const topVersion = changelog.match(/^\* ([0-9]+\.[0-9]+\.[0-9]+)\b/m)?.[1];

if (pkg.version !== topVersion) {
  throw new Error(`package.json version ${pkg.version} does not match CHANGELOG ${topVersion}`);
}

if (pkg.license !== 'CC-BY-NC-SA-4.0' || !readme.includes('CC BY-NC-SA 4.0')) {
  throw new Error('package.json license must match README license');
}
