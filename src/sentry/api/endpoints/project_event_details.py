from __future__ import absolute_import

import six
import logging
from uuid import uuid4

from rest_framework.response import Response

from sentry.api.base import DocSection
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.serializers import serialize
from sentry.models import Event
from sentry.utils.apidocs import scenario, attach_scenarios
from sentry.api.filters.response_wrapper import add_post_method

delete_logger = logging.getLogger('sentry.deletions.api')

@scenario('RetrieveEventForProject')
def retrieve_event_for_project_scenario(runner):
    runner.request(
        method='GET',
        path='/projects/%s/%s/events/%s/' %
        (runner.org.slug, runner.default_project.slug, runner.default_event.event_id)
    )


@add_post_method
class ProjectEventDetailsEndpoint(ProjectEndpoint):
    doc_section = DocSection.EVENTS

    @attach_scenarios([retrieve_event_for_project_scenario])
    def get(self, request, project, event_id):
        """
        Retrieve an Event for a Project
        ```````````````````````````````

        Return details on an individual event.

        :pparam string organization_slug: the slug of the organization the
                                          event belongs to.
        :pparam string project_slug: the slug of the project the event
                                     belongs to.
        :pparam string event_id: the hexadecimal ID of the event to
                                 retrieve (as reported by the raven client).
        :auth: required
        """
        try:
            event = Event.objects.get(
                event_id=event_id,
                project_id=project.id,
            )
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=404)

        Event.objects.bind_nodes([event], 'data')

        # HACK(dcramer): work around lack of unique sorting on datetime
        base_qs = Event.objects.filter(
            group_id=event.group_id,
        ).exclude(id=event.id)
        try:
            next_event = sorted(
                base_qs.filter(datetime__gte=event.datetime).order_by('datetime')[0:5],
                key=lambda x: (x.datetime, x.id)
            )[0]
        except IndexError:
            next_event = None

        try:
            prev_event = sorted(
                base_qs.filter(
                    datetime__lte=event.datetime,
                ).order_by('-datetime')[0:5],
                key=lambda x: (x.datetime, x.id),
                reverse=True
            )[0]
        except IndexError:
            prev_event = None

        data = serialize(event, request.user)

        if next_event:
            data['nextEventID'] = six.text_type(next_event.event_id)
        else:
            data['nextEventID'] = None
        if prev_event:
            data['previousEventID'] = six.text_type(prev_event.event_id)
        else:
            data['previousEventID'] = None

        return Response(data)

    def delete(self, request, project, event_id):
        """
        Remove an Event
        ```````````````

        """
        # from sentry.tasks.deletion import delete_event
        try:
            event = Event.objects.get(
                event_id=event_id,
                project_id=project.id,
            )
            # TODO: Since other api use apply_async
            # for sending task to redis, this method
            # should rewrite with apply_async.
            event.delete()
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=404)

        transaction_id = uuid4().hex
        self.create_audit_entry(
            request=request,
            organization_id=project.organization_id if project else None,
            target_object=event.id,
            transaction_id=transaction_id,
        )

        delete_logger.info(
            'object.delete.queued',
            extra={
                'object_id': event.id,
                'transaction_id': transaction_id,
                'model': type(event).__name__,
            }
        )
        return Response(status=202)

        # delete_event.apply_async(
        #     kwargs={
        #         'object_id': event.id,
        #         'transaction_id': transaction_id,
        #     },
        #     countdown=3600,
        # )