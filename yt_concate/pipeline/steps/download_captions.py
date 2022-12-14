import time

import pytube
from pytube import YouTube

from yt_concate.pipeline.steps.log import config_logger
from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException


class DownloadCaption(Step):
    def process(self, data, inputs, utils):
        logging = config_logger()
        # download the package by:  pip install pytube
        start = time.time()
        for yt in data:
            logging.info('downloading caption for{}'.format(yt.id))
            if utils.caption_file_exists(yt):
                logging.info('find existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError, pytube.exceptions.RegexMatchError):
                logging.warning('Error when downloading caption for {}'.format(yt.url))
                continue

            # save the caption to a file named Output.txt
            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

        end = time.time()
        logging.debug(f'took{end - start}s')

        return data
