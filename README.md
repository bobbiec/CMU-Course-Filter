# CMU-Course-Filter
Hi Karina! This is a poorly-made utility to filter courses for CMU schedule planning

Dependencies:
- [CMU-Course-API](https://github.com/ScottyLabs/course-api)
  - Not technically required to run filter but it was used to generate f17.json

Issues:
- Duplicate courses for unknown reason
- No location filtering (so results include Qatar, etc)
- Really ugly text output, but who cares
  - No way to identify linked courses (Tu-Thu lectures, for example)
  - Text output makes it hard to see overlapping courses
