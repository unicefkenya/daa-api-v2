# Duplicate Command

- Command name is `duplicate`

- Use to determine and merge duplicate learners

## Process
- Unique learners are identified using, `stream_id`, `first_name`, `middle_name`, `upi`, `date_of_birth`.

- Refere to the `STUD_UNIQUE_NAME_CLASS` definition in `school.models.STUD_UNIQUE_NAME_CLASS`

- Learner with most attendances is identified as the main learner.

- All `attendances` and `Reason for Absence` for the other learners are merged into the main learner.

**NOTE**: *Duplicate attendances are not identified as of now* 


## Options
|Name|Choices|Descriptions|Example|
|:--|:--|:--|:--|
|`--dry-run`|`true` ,`false`|When `false` duplicate learners and merged and deleted permanently|`--dry-run=false`|
|`--dry-run-count`|An integer|Used together with `--dry-run=true`. When number of affected learners is reached the script quits.| `--dry-run-count=1000`|
|`--only`|`all`, `imports`|Used to filter learners list with `imports` as only the days an import was triggered.| `--only=imports`|



