# Reporting a security problem

This policy covers the course instructions, authoring scripts, and downloadable release ZIP. Examples include a real credential in an archive, a guest command that could erase host data, or a network configuration that exposes a deliberately vulnerable VM.

**During private review:** contact the maintainer privately through the channel used to arrange your review. If you have no private contact, open an issue asking only for a secure contact method. Do not include vulnerability details in the issue.

**After public launch:** if the repository's Security tab offers **Report a vulnerability**, use it to send a private report. If that option is unavailable, ask for a secure contact method as described above.

Include the release tag, filename or lesson and step, the potential impact, and a sanitized description of what you observed. Do not include passwords, tokens, personal data, or sensitive logs. You do not need to reproduce a destructive command to report it.

For broken links, unclear wording, and ordinary setup questions, use the repository's question or correction issue template. For a flaw in third-party software itself, use that vendor's security reporting channel; let the course maintainer know separately if the lab instructions need to change.
