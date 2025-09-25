from marshmallow import Schema, fields, validate, ValidationError, post_load


class OptionSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    is_correct = fields.Bool(required=True)


class QuestionCreateSchema(Schema):
    text = fields.Str(required=True, validate=validate.Length(min=1))
    type = fields.Str(required=True, validate=validate.OneOf(['single','multiple','text']))
    max_words = fields.Int(required=False)
    options = fields.List(fields.Nested(OptionSchema), required=False)


    @post_load
    def check_options(self, data, **kwargs):
        qtype = data.get('type')
        opts = data.get('options') or []

        if qtype in ('single','multiple'):
            if not opts or len(opts) < 2:
                raise ValidationError('Choice questions must have at least two options.')
            correct_count = sum(1 for o in opts if o.get('is_correct'))
            if qtype == 'single' and correct_count != 1:
                raise ValidationError('Single choice questions must have exactly one correct option.')
            if qtype == 'multiple' and correct_count < 1:
                raise ValidationError('Multiple choice questions must have at least one correct option.')
        elif qtype == 'text':
            # ensure no options for text
            if opts:
                raise ValidationError('Text questions should not have options.')
            max_words = data.get('max_words')
            if max_words is None:
                data['max_words'] = 300
            elif max_words > 1000:
                raise ValidationError('max_words too large; keep under 1000.')

        return data


class QuizCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))


class SubmitAnswerItemSchema(Schema):
    question_id = fields.Int(required=True)
    selected_option_ids = fields.List(fields.Int(), required=False)
    text_answer = fields.Str(required=False)


class SubmitAnswersSchema(Schema):
    answers = fields.List(fields.Nested(SubmitAnswerItemSchema), required=True)