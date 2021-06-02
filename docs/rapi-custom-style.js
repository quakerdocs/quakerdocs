import { css } from 'lit-element';

export default css`
nav.nav-scroll {
    border-top: 1px solid #ccc;
    scrollbar-color: #ccc transparent !important;
}

nav.nav-scroll::-webkit-scrollbar-thumb {
    background-color: #ccc !important;
}

schema-tree, .example-panel {
    max-height: 500px;
    overflow-y: auto;
}
`;
