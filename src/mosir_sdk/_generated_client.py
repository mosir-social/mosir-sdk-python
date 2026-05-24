from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from typing import Any, Protocol

from ._operations import OPERATION_REGISTRY


class _ClientProtocol(Protocol):
    async def request(
        self,
        document: str,
        variables: Mapping[str, Any] | None = None,
        *,
        operation_name: str | None = None,
    ) -> dict[str, Any]: ...

    def subscribe(
        self,
        document: str,
        variables: Mapping[str, Any] | None = None,
        *,
        operation_name: str | None = None,
    ) -> AsyncIterator[dict[str, Any]]: ...


def _normalize_variables(variables: dict[str, Any], variable_map: dict[str, str]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in variables.items():
        normalized[variable_map.get(key, key)] = value
    return normalized


class GeneratedOperationMethods:
    """Generated snake_case wrappers from public.operations.graphql."""

    async def get_account_profile(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_account_profile']
        variable_map = {'accountId': 'accountId', 'account_id': 'accountId', 'username': 'username'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_blocked_accounts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_blocked_accounts']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_current_account(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_current_account']
        variable_map = {}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_discussions(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_discussions']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_feed_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_feed_posts']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_followed_accounts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_followed_accounts']
        variable_map = {'accountId': 'accountId', 'account_id': 'accountId', 'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_followed_post_collections(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_followed_post_collections']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_following_accounts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_following_accounts']
        variable_map = {'accountId': 'accountId', 'account_id': 'accountId', 'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_following_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_following_posts']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_history_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_history_posts']
        variable_map = {'cursor': 'cursor', 'includeOwnPosts': 'includeOwnPosts', 'include_own_posts': 'includeOwnPosts', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_link_preview(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_link_preview']
        variable_map = {'url': 'url'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_media(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_media']
        variable_map = {'mediaId': 'mediaId', 'media_id': 'mediaId'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_mutual_followers(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_mutual_followers']
        variable_map = {'accountId': 'accountId', 'account_id': 'accountId', 'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_my_post_collections(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_my_post_collections']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_notifications(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_notifications']
        variable_map = {'cursor': 'cursor', 'filter': 'filter', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_popular_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_popular_posts']
        variable_map = {'cursor': 'cursor', 'language': 'language', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post']
        variable_map = {'postId': 'postId', 'post_id': 'postId'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_collection(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_collection']
        variable_map = {'id': 'id'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_collections_by_author(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_collections_by_author']
        variable_map = {'authorID': 'authorID', 'author_id': 'authorID', 'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_draft(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_draft']
        variable_map = {'id': 'id'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_drafts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_drafts']
        variable_map = {'cursor': 'cursor', 'filter': 'filter', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_drafts_count(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_drafts_count']
        variable_map = {'filter': 'filter'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_reaction_details(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_reaction_details']
        variable_map = {'cursor': 'cursor', 'limit': 'limit', 'postId': 'postId', 'post_id': 'postId', 'type': 'type'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_post_reactions(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_post_reactions']
        variable_map = {'first': 'first', 'postId': 'postId', 'post_id': 'postId'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_profile_tag_by_id(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_profile_tag_by_id']
        variable_map = {'id': 'id'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_profile_tag_profiles(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_profile_tag_profiles']
        variable_map = {'cursor': 'cursor', 'limit': 'limit', 'tagId': 'tagId', 'tag_id': 'tagId'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_reacted_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_reacted_posts']
        variable_map = {'cursor': 'cursor', 'limit': 'limit', 'reactionType': 'reactionType', 'reaction_type': 'reactionType'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_topic_feed_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_topic_feed_posts']
        variable_map = {'cursor': 'cursor', 'limit': 'limit', 'topicId': 'topicId', 'topic_id': 'topicId'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_topics(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_topics']
        variable_map = {'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_unread_notification_count(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_unread_notification_count']
        variable_map = {}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_user_posts(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_user_posts']
        variable_map = {'accountId': 'accountId', 'account_id': 'accountId', 'cursor': 'cursor', 'limit': 'limit', 'postType': 'postType', 'post_type': 'postType'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def get_user_reactions(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['get_user_reactions']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    async def list_profile_tags(self: _ClientProtocol, **variables: Any) -> dict[str, Any]:
        spec = OPERATION_REGISTRY['list_profile_tags']
        variable_map = {'cursor': 'cursor', 'limit': 'limit'}
        return await self.request(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    def notification_received(self: _ClientProtocol, **variables: Any) -> AsyncIterator[dict[str, Any]]:
        spec = OPERATION_REGISTRY['notification_received']
        variable_map = {}
        return self.subscribe(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    def post_created_by_author(self: _ClientProtocol, **variables: Any) -> AsyncIterator[dict[str, Any]]:
        spec = OPERATION_REGISTRY['post_created_by_author']
        variable_map = {'authorId': 'authorId', 'author_id': 'authorId', 'postType': 'postType', 'post_type': 'postType'}
        return self.subscribe(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    def post_created_in_collection(self: _ClientProtocol, **variables: Any) -> AsyncIterator[dict[str, Any]]:
        spec = OPERATION_REGISTRY['post_created_in_collection']
        variable_map = {'postCollectionID': 'postCollectionID', 'post_collection_id': 'postCollectionID'}
        return self.subscribe(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    def post_deleted(self: _ClientProtocol, **variables: Any) -> AsyncIterator[dict[str, Any]]:
        spec = OPERATION_REGISTRY['post_deleted']
        variable_map = {'postId': 'postId', 'post_id': 'postId'}
        return self.subscribe(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    def post_updated(self: _ClientProtocol, **variables: Any) -> AsyncIterator[dict[str, Any]]:
        spec = OPERATION_REGISTRY['post_updated']
        variable_map = {'postId': 'postId', 'post_id': 'postId'}
        return self.subscribe(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )

    def reply_created_under_root_post(self: _ClientProtocol, **variables: Any) -> AsyncIterator[dict[str, Any]]:
        spec = OPERATION_REGISTRY['reply_created_under_root_post']
        variable_map = {'rootPostId': 'rootPostId', 'root_post_id': 'rootPostId'}
        return self.subscribe(
            spec.document,
            _normalize_variables(variables, variable_map) or None,
            operation_name=spec.operation_name,
        )
